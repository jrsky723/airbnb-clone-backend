# Day 1

django 프레임 워크를 이용하여 Airbnb-backend를 clone한다

프로젝트는 poetry를 이용하여 관리

## 1. 프로젝트 생성

- django 프로젝트를 시작할때, 명령어 "django-admin startproject"를 사용한다.

## 2. 프로젝트 설정

- 초기에 자동으로 생성된 migration들을 적용한다.

- migration: 데이터베이스의 스키마를 버전 관리하는 것

## 3. 앱 생성

- House application을 생성한다
- app : django에서는 app을 모듈로 인식한다. app은 하나의 기능을 담당한다.
- 따라서 airbnb의 House app은 House와 관련된 기능을 담당한다.
- model안에 무엇을 수정하면, database에게 알려줘야함. migration을 생성 후 migrate
- django의 admin 관리 패널에서 확인 할 수 있다.

- migration 파일은 django가 파이선 코드를 사용해서 sql을 만들어주는 것이다.
