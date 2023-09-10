# 11 REST API

- api를 직접 만들어 볼 것이다.
- 보안을 여기선 신경을 쓰진 않을 것이다. 저번 섹션의 연습시간

- rooms/amenity의 api를 만들기
  - read only : created_at, updated_at

## 11.3 Rooms

- 여기서는 추가적인 기능이 필요하다
  - Autentication
    - Room의 host만이 수정할 수 있어야 한다.
  - Relationship
    - api에서 정보를 주고 받을때, id만 주고 받는 것이 아니라, 다른 정보들도 주고 받을 수 있어야 한다.
    - depth를 부여한다면, 이러한 기능을 구현할 수 있다.
    - 하지만 모든 정보를 주고 받는 것은 비효율적이다.
    - rooms : 사진, 리뷰, 유저, 룸타입, 편의시설
    - room : 더 자세한 detail <-- 이곳에서 relationship을 통해 정보를 주고 받을 수 있다.
  - serializer를 두 개로 나눈다.

## 11.4 Room Detail

- room detail을 위한 serializer를 만들어 보자.
- user의 정보를 자세하게 (단 모든 정보가 아닌) 주고 받을 수 있도록 하자.
- user에 TinyUserSerializer를 만들고, room에 이를 적용하자.
  - owner = TinyuserSerializer()

## 11.5 Create Room

- room을 create할떄 필수 항목에 relationship이 포함되어있다. (User)
- user에게 owner를 변경할 권한을 주면 안된다.

  - user의 data에서 오지 않을 것이다.

- amenities와 category는 db에 있어야한다. (manytomany, foreignkey)
- 아니면 room이 생성되지 않고, 오류 발생
- owner는 request.user이다.
- user가 authenticated 되어있는지 확인해야한다.
- save()에 user를 넣어주면, Serializer의 create에 validated_data에 user가 추가된다.

## 11.6 Room Amenities

- api를 테스트 할때, serialize의 create의 return을 비워놓는다.
- error가 발생할 수 있는 부분은 try except로 감싸준다.
- amenities와 room은 many to many 관계
  - room.amenities.add()로 추가 할 수 있음

## 11.9 Transactions

- Room이 생성된 후에 amenities를 추가하는 작업을 하고 있기 때문에, amenities를 추가하는 과정에서 오류가 발생해도, room이 db에 남게 된다.
- 하지만 delete를 많이 하게되면, id가 빈 공간이 많아지게 된다.
- 이를 방지하기 위해 transaction을 사용한다.
  - 많은 쿼리들이 생성되거나, 삭제되는 작업을 하나의 작업으로 묶어준다.
  - 하나의 작업이라도 실패하면, 모든 작업이 취소된다.
  - django의 transaction을 이용하면, 어떤 코드 조각이 실패하면, 모든 작업이 취소되고, db를 원래 상태로 되돌린다.
- transaction.atomic(): 안에 코드를 둔다면, 모든 코드가 하나의 작업으로 묶인다.
- try-catch를 안에 두면, transaction이 오류가 생겼는지를 모른다.

## 11.11 SerializerMethodField

- SerializerMethodField를 이용하면, serializer에 method를 추가할 수 있다.
- method의 이름은 get\_로 시작해야한다.
- model안의 method를 사용할 수 있음

## 11.12 Serializer Context

- serializer에 context를 추가할 수 있다.
- context에 request를 넣어서, is_owner를 구현

## 11.13 Reverse Serializers

- room의 review는 review에서 foriegnkey로 room을 가지고 있다.
  - 이는 room에 자동적으로 review_set이 생긴다는 것을 의미한다.
- 이런 방법으로 review를 RoomDetailSerializer에 추가할 수 있다.
  - 하지만, 모든 review를 보여줌으로, 페이지를 추가해서 한 번에 5~10개만 보여주도록 한다.

## 11.14 Pagination

- pagination을 위해, django-rest-framework의 pagination을 사용한다.
- pagination: 페이지를 나누어서 보여주는 것
  - 예를 들어 인스타그램의 좋아요는 user당 엄청 많을 수 있다, 이를 한 페이지에 모두 보여주면, 통제가 불가능

## 11.5 File Uploads

- 사진을 업로드 하면 자동으로 저장되는 위치를 변경해줘야한다.
- conifg/settings.py에 MEDIA_ROOT를 추가한다.
- config/urls.py에 static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)를 url pattern에 추가해서, media url을 static url로 사용할 수 있도록 한다.
- 개발단계에서는 media를 저장할 수 있는 url을 만든다.
  - 실제 서비스 환경에서는 보안 문제가 생긴다
  - 인증이 되지 않은 사람들이 파일을 업로드 할 수 있도록 허락하는 것이다.
  - 파일들이 코드 옆에 저장되는 것이 아니라, 다른 곳에 저장되어야 한다.
  - 이를 방지하기 위해 aws을 이용하여 파일을 저장한다.

## 11.17 permission_classes

- photo의 DELETE api를 구현하기
  - api의 url이 DELETE /rooms/1/photos/1이여야할까?
  - 아니면 DELETE /medias/photos/1 이도록 하자
- permission_classes에 IsAuthenticated를 추가하면, 로그인이 되어있는지 확인할 수 있다.
- 하지만, room 같은 경우, 어떤 request는 모든 유저가, 어떤 request는 owner만이 할 수 있도록 해야한다.
- 이럴때는 IsAuthenticatedOrReadOnly를 사용한다.
  - get request는 모든 유저가 할 수 있고, post, put, delete는 owner만 할 수 있도록 한다.

## 11.18 Reviews

- 방의 review를 GET, POST 한다.
  - 유저, 페이로드, 평점만 원함 (url에 room의 id가 있으므로)

## 11.19 WishLists

- user의 wishlist API를 구현
- WishLists에서 room을 보여줄때, RoomListSerializer를 사용하는데, 이때, get_is_owner에서 context의 request를 찾는다.
- 그러므로 context에 request를 넣어줘야한다.

## 11.20 Wishlists

- 이제 wishlist안의 room을 수정하길 원한다
- 하나의 room을 얻을때, filter를 사용하고, exists()를 사용해서, room이 wishlist에 있는지 확인한다.
- 만약 user가 wishlist안에 있는 room을 put하면, room을 삭제하고, 없는 room을 put하면, room을 추가한다.

## 11.21 is_liked

- room list에서 room이 wishlist에 포함되어있는지를 보여주고싶다.
- wishlist의 filter에 user는 request.user이고, rooms\_\_pk는 room의 pk이다.

## 11.22 Bookings

- 로그인 한 유저에게 room의 booking을 보여준다.
- **_ django import convention _**

  - django package에서 나오는 것을 먼저 import
  - third-party package를 import (rest_framework)
  - 같은 앱에 있는 것을 import
  - 다른 앱에 있는 것을 import

- user가 존재하는 room에 대해서만 booking을 한다고 가정하면, 코드가 더 간단해진다.
  - filter로 room\_\_pk를 이용하면, room에 해당하는 booking을 찾을 수 있다.
- booking에서는 시간을 사용하기 때문에 timezone을 import한다.
- django timezone은 나의 config/settings.py에 있는 TIME_ZONE을 사용한다.
- booking을 찾을때 현재 시간보다, check_in 시간이 더 큰 (미래의) booking을 찾는다.

## 11.23 Create a Booking

- booking의 GET & POST
- booking serializer에서 guest말고, check_in, check_out field가 필수적이 아닐 수도 있다.
- 데이터 생성 용으로 사용하는 serializer와 데이터를 보여주는 serializer를 분리한다.
- 나만의 validation 기준이 있다면?
  - serializer에서 custom validation을 넣을 수 있을까?
    - user가 과거의 check_in을 보냈을때, is_valid()가 false를 반환하도록 할 수 있을까?
  - 이런경우, validate\_필드명()을 사용한다.
    - 이는 serializer의 필드를 검증하는 함수이다.
    - 이 함수는 필드의 값이 올바르지 않으면, ValidationError를 발생시킨다.
    - 이를 이용해서, check_in이 check_out보다 빠른지를 검증할 수 있다.
  - value를 return하면, validation이 통과 되었다는 뜻이다.
- to-do validations
  - check_in이 check_out보다 빠른지
  - 겹치는 booking이 있는지

## 11.24 Validate Booking

- validate() 함수는 serializer의 모든 필드를 검증한다.
- user가 원하는 날짜에 겹치는 booking이 있는지 확인하기 위해
  - filter(check_in**lte=check_out, check_out**gte=check_in)을 사용한다.

## 11.25 Booking Completed
