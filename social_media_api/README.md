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


Posts & Comments API Endpoints
1. List All Posts
URL: /api/posts/
Method: GET
Auth Required: 
Description: Retrieve a paginated list of all posts.

2. Create a New Post
URL: /api/posts/
Method: POST
Auth Required: 

3. Retrieve a Single Post
URL: /api/posts/<id>/
Method: GET
Auth Required: 

4. Update a Post
URL: /api/posts/<id>/
Method: PUT or PATCH
Auth Required:  (only the author can update)

5. Delete a Post
URL: /api/posts/<id>/
Method: DELETE
Auth Required:  (only the author can delete)


Comments Endpoints
1. List Comments for a Post
URL: /api/posts/<post_id>/comments/
Method: GET
Auth Required: 

2. Add a Comment to a Post
URL: /api/posts/<post_id>/comments/
Method: POST
Auth Required: 

3. Update a Comment
URL: /api/comments/<id>/
Method: PUT or PATCH
Auth Required: (only the author can update)

4. Delete a Comment
URL: /api/comments/<id>/
Method: DELETE
Auth Required: (only the author can delete)


Follows & Feed API
1. POST /api/accounts/follow/<user_id>/  - follow user with id
   Requires auth
   Response: {"detail":"Followed."}

2. POST /api/accounts/unfollow/<user_id>/  - unfollow
   Requires auth
   Response: {"detail":"Unfollowed."}

3. GET /api/accounts/following/  - list users you follow
   Requires auth

4. GET /api/posts/feed/  - list posts from users you follow (newest first)
   Requires auth
   Optional: use pagination query params if enabled.

Notes:
- Only authenticated users can modify follow relationships.
- You cannot follow yourself (API returns 400).
- Changing the `following` field is done only by the authenticated user (server uses request.user.following.add/remove).


Notifications & Likes API
Models:
- posts.Like: post FK, user FK, unique_together (post,user)
- notifications.Notification: recipient, actor, verb, generic target, read, timestamp

APIs:
- POST /api/posts/<post_id>/like/    - like post (auth required)
- POST /api/posts/<post_id>/unlike/  - unlike post (auth required)
- GET  /api/notifications/           - list notifications for current user (auth required)
- POST /api/notifications/<id>/mark-read/ - mark a notification read

Notes:
- A notification is automatically created when someone likes your post, and when someone follows you (if you add that in follow view).
- Notification target uses GenericForeignKey so it can point to a Post, Comment, or other object.
- Future: consider WebSockets / Django Channels for real-time notifications.
