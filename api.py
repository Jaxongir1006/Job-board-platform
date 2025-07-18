from ninja_extra import NinjaExtraAPI
from users.controllers import RegisterAndLoginController, UserController
from jobs.controllers import JobsController

api = NinjaExtraAPI()

api.register_controllers(RegisterAndLoginController, UserController, JobsController)