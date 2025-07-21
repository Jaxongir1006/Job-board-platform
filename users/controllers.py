from ninja_extra import (
    api_controller,
    http_get,
    http_post,
    http_put,
    http_delete,
)
from .schemas import (
    RegisterSchema,
    LoginSchema,
    UserSchema,
    UserProfileSchema,
    UserResponseSchema,
    UpdateUserSchema,
    ChangePasswordSchema,
)
from .models import CustomUser, UserProfile
from ninja_jwt.tokens import RefreshToken
from ninja.errors import HttpError
from utils.permissions import IsAuthenticatedAndNotDeleted
from ninja_jwt.authentication import JWTAuth
import logging

logger = logging.getLogger("__name__")



@api_controller("", tags=["Register and Login"])
class RegisterAndLoginController:
    @http_post("/register/", response=UserResponseSchema)
    def register(self, request, data: RegisterSchema):
        data = data.model_dump()
        if data["password"] != data["confirm_password"]:
            return HttpError(400, "Passwords do not match")
        data.pop("confirm_password")
        if data["user_type"] == "admin" and not request.user.is_superuser:
            logger.error("Unauthorized attempt to create admin user")
            return HttpError(400, "You don't have permission to create admin")
        user = CustomUser.objects.create_user(**data)
        logger.info(f"User {user.username} registered successfully.")
        UserProfile.objects.create(user=user)
        token = RefreshToken.for_user(user)
        return {
            "user": UserSchema.from_orm(user),
            "tokens": {
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            },
        }

    @http_post("/login/", response=UserResponseSchema)
    def login(self, request, data: LoginSchema):
        data = data.model_dump()
        user = (
            CustomUser.objects.filter(email=data["login_input"]).first()
            or CustomUser.objects.filter(username=data["login_input"]).first()
            or CustomUser.objects.filter(phone_number=data["login_input"]).first()
        )
        if user.is_deleted:
            logger.error(f"Login attempt by deleted user: {user.username}")
            return HttpError(400, "The user has been deleted")
        if not user:
            logger.error("User not found for login attempt")
            return HttpError(400, "User not found")
        if not user.check_password(data["password"]):
            logger.error(f"Invalid password for user: {user.username}")
            return HttpError(400, "Invalid password")
        token = RefreshToken.for_user(user)
        return {
            "user": UserSchema.from_orm(user),
            "tokens": {
                "access_token": str(token.access_token),
                "refresh_token": str(token),
            },
        }


@api_controller("user/", tags=["Users"], auth=JWTAuth(), permissions=[IsAuthenticatedAndNotDeleted])
class UserController:

    @http_get("me/", response=UserProfileSchema)
    def me(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        return UserProfileSchema(
            first_name=profile.first_name,
            last_name=profile.last_name,
            profile_picture=(
                profile.profile_picture.url if profile.profile_picture else None
            ),
            age=profile.age,
            location=profile.location,
            about=profile.about,
            skills=profile.skills,
            cv=profile.cv.url if profile.cv else None,
            user=UserSchema.from_orm(request.user),
        )

    @http_put("me/", response=UserProfileSchema)
    def update_my_profile(self, request, data: UpdateUserSchema):
        user = request.user
        profile = UserProfile.objects.get(user=user)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, field, value)
        logger.info(f"User {user.username} updated their profile.")
        profile.save()
        return UserProfileSchema(
            first_name=profile.first_name,
            last_name=profile.last_name,
            profile_picture=(
                profile.profile_picture.url if profile.profile_picture else None
            ),
            age=profile.age,
            location=profile.location,
            about=profile.about,
            skills=profile.skills,
            cv=profile.cv.url if profile.cv else None,
            user=UserSchema.from_orm(request.user),
        )

    @http_delete("me/", response=dict)
    def delete_my_profile(self, request):
        user = request.user
        logger.info(f"User {user.username} deleted their account.")
        user.delete()
        return {"message": "User deleted successfully"}

    @http_put("me/password/", response=dict)
    def change_password(self, request, data: ChangePasswordSchema):
        if not request.user.check_password(data.old_password):
            return {"message": "Old password is incorrect"}
        if data.new_password != data.confirm_password:
            return {"message": "New passwords do not match"}
        logger.info(f"User {request.user.username} changed their password.")
        request.user.set_password(data.new_password)
        request.user.save()
        return {"message": "Password changed successfully"}

