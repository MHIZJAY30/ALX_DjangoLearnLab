Social Media API

This is the Social Media API built with Django and Django REST Framework as part of the ALX Django Learn Lab project.
The project implements user authentication and a custom user model with extended fields.


Features
Custom User Model with:
bio (TextField)
profile_picture (ImageField)
followers (ManyToMany to User, a symmetrical)
User Registration (with token generation)
User Login (with token retrieval)
User Profile Management (view & update profile)
Token Authentication using DRF


User Model Overview
The custom user model extends Django’s AbstractUser with additional fields:
bio → text field for user biography
profile_picture → optional image field
followers → many-to-many relationship with other users