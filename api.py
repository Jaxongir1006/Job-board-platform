from ninja_extra import NinjaExtraAPI
from users.controllers import RegisterAndLoginController, UserController
from jobs.controllers import JobsController
from favourite_jobs.controller import FavouriteJobsController
from applications.controller import JobApplicationController

api = NinjaExtraAPI()

api.register_controllers(RegisterAndLoginController, UserController, JobsController, FavouriteJobsController, JobApplicationController)