# 12 USER API

- GET PUT /me [x]
- POST /users
- POST /users/log-in
- POST /user/change-passwod
- POST /users/github

## 12.0 User Profile

- /me 를 만든다. private url이고 자신의 프로필을 받아온다.
- 공개 프로필을 받아올때는 /users/username을 이용
  - 따라서 fullUserSerializer & PublicUserSerializer를 만든다.
- from . import ~ 를 통해 import문을 줄일 수 있다.
- admin 패널에서 관리하는 attribute는 exclude한다.

## Create USer

## Change Password

## Log in and Log Out
