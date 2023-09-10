# Day 3

## 7 ORM

- ORM: Object Relational Mapping (관계형 데이터베이스를 객체지향적으로 사용하기 위한 기술)
- 어떻게 database와 소통할지
- 어드민 패널 사용없이 데이터를 코딩으로 직접 소통하는 방법
- django의 shell을 열어서 파이썬 코드를 작성, (shell안에있어야함)

- `python manage.py shell` : shell을 열어줌, django에 있는 모든 코드를 사용할 수 있음
- get method로 데이터를 가져올 수 있음
- foriegn key를 사용한 데이터는 그대로, .으로 연결해서 가져올 수 있음
- save()로 저장

- basic operations

  - all: 모든 데이터를 가져옴
  - filter: 조건에 맞는 데이터를 가져옴
    - gt, gte, lt, lte, contains, startswith, endswith
  - get: 조건에 맞는 데이터를 하나만 가져옴
    - 조건에 맞는 데이터가 없거나, 2개 이상이면 오류 발생
  - exclude: 조건에 맞지 않는 데이터를 가져옴
  - order_by: 데이터를 정렬해서 가져옴

- QuerySets

  - 계속 filter를 적용할 수 있음
  - QuerySets는 실제 데이터가 아닌, 데이터를 가져오는 방법을 저장한 것
  - lazy한 특성을 가지고 있음
  - 해당 데이터를 이용할때(ex: print), 실제 데이터를 가져옴
  - get은 실제 데이터를 가져오기 때문에, QuerySets가 아님

- lookup

  - \_\_: 언더바 두개
  - lookup을 사용하면, 데이터베이스에서 데이터를 가져올 때, 조건을 추가할 수 있음
  - case sensitive: 대소문자 구분
    - i: 대소문자 구분하지 않음 (insensitive)
  - 연결해서 사용 가능
    - **gt**lte

- 어드민 패널 & 모델 중 어디에 함수를 생성할지 정한다.

- reverse accessor:

  - 관계를 뒤집어서 접근할 수 있음
  - foreignkey에 접근해서, 그 foreignkey를 가지고 있는 객체를 찾아올 수 있음
  - room 의 owner가 얼마나 많이 room을 가지고 있는지 알고 싶을 때
  - 1 : owner\_\_username
    - \_\_foreignkey + ~ : reverse accessor
  - 2 : owner.room_set.all()
    - room_set : reverse accessor
    - room_set.all() : room_set에 있는 모든 room을 가져옴

- Foreignkey를 부여한 객체는, 자동으로 \_\_set을 갖게된다.
- related_name을 설정하면, \_\_set을 설정한 이름으로 사용할 수 있다.

- python dir : 객체가 가지고 있는 모든 속성을 보여줌

- query optimization

  - 필요한 값만 value로 가져오기

- search_fields

  - ^ : startswith

- action
  - 3개의 매개변수를 받는 함수를 만들어야함
    - model_admin, request, queryset
    - request: 요청을 보낸 유저
    - queryset: 선택된 객체들

## 9 URLS AND VIEWS

- urls.py : url을 관리하는 파일
- views.py : 함수를 관리하는 파일

  - 파일이름 변경 가능
  - views.py 에 있는 함수는 request object를 자동으로 받는다.
  - request : 브라우저의 정보, 전송하고 있는 데이터, 쿠키 등등

- 각각 폴더별로 urls.py를 생성하고, 안의 urlpatterns를 import해서 사용할 수 있다.

- 여러개의 방을 보는 화면과, 하나의 방을 보는 화면이 필요

- django template system:

  - flask와 유사하다.

- 왜 template을 안 쓰는지
  - template을 쓰면, html을 만들어야함
  - 다이나믹 web을 만들기가 힘들다.
  - front에서 react를 사용한다.

# DJANO REST FRAMEWORK

- poetry add djangorestframework
- INSTALLED_APPS에 추가
- 필요한 API만 만들면 한다.
  - GET or POST
- django serializer
  - python object를 json으로 바꿔줌
- Django REST 프레임워크를 사용하지 않고, 직접 만들 수도 있다.

  - 하지만, REST 프레임워크를 사용하면, 더 쉽게 만들 수 있다.

- object를 serialize 하기 위해, serializers.py를 생성
- category가 api로 나갈때 어떻게 나갈지를 정해줄 수 있음.
- model을 생성할 때 처럼, serializer도 생성해줘야함
- post request를 바로 db에 적용하면안된다. validation 필요
- data를 user로 부터 받아서, django object로 만들려면, serializer를 사용해야함
- serializer validation

  - GET & POST 시에 둘 다 가능

- serializer.save()

  - serializer는 create를 찾아서, create를 실행한다.

- PUT: update

  - serializer의 partial=True를 사용하면, 부분적으로 업데이트 가능
  - django가 update를 찾아서 실행한다.
  - serializer에 data를 설명해주면, user가 보낸 data를 검증할 수 있다.
  - serializer에 data가 새로 생기면, create를 실행한다.
    - update를 실행하려면, instance를 넣어줘야함

- 우리가 작성한 serializer 코드는 전부 지울 것이다.
