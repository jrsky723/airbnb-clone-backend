# day2

## 앱 설정 변경

- admin 패널에서 뜨는 객체의 이름을 변경하고 싶다면, str method를 변경할 것

## admin 패널 column 변경

- admin.py에서 list_display를 입력하여서 보여줄 column을 수정할 수 있다.
- django 에선 list 대신 tuple을 사용한다.
- django documentation을 참고하면 더 많은 옵션을 확인할 수 있다.

# 5.USER APPS

- user app을 만들어서 user를 관리할 수 있다.
- user profile photo, social login 등을 관리할 수 있다.
- 프로젝트를 시작할 때, custom user model을 생성하는 것이 더 좋다.

- django는 가상환경에만 설치되어있으므로, python interpreter를 변경해야한다.

- django에서 제공하는 user를 사용해야하므로, import를 추가로 하고 상속받도록한다.

- 사용자가 없는 상태에서 해야한다. db초기화

- Booleanfield는 non-nullable이므로, default값을 설정해야한다.
- 이미 생성된 superuser과 충돌
- model에서는 firtname과 lastaname을 non-editable로 설정했지만, admin 패널에서는 수정이 가능하므로, 충돌
- house와 user를 연결 해줘야한다.
- on_delete=models.CASCADE : user가 삭제되면, house도 삭제된다.
- default는 예전 데이터를 위한 것인다.

## 6.MODELS AND ADMIN

- **init**.py: 해당 폴더가 python package임을 알려주는 파일
- user photo 생성 시에, pillow를 추가하는데, poetry add Pillow를 통해 추가한다.
- choices를 추가할 수 있다 (value, label: db에서 나올 이름)
- rooms model 생성
- amenities model 생성 (many to many 관계)
- relationship

  - Many To One : ForeignKey
  - Many To Many : ManyToManyField
    - ManyToManyField는 admin 패널에서 추가할 수 있는 기능을 제공한다.
  - One To One : OneToOneField

- CommonModel

  - 모든 모델에 abstract model을 추가할 수 있다.
  - created_at, updated_at
  - class Meta: abstract=True : db에는 생성되지 않는다.

- Expriences

  - airbnb에서는 host가 experience를 생성한다.

- Reviews

  - user가 review를 생성한다.

- wishlists

  - user가 wishlist를 생성한다.

- bookings

  - user가 room을 예약한다.
  - room은 여러번 예약될 수 있다.
  - user는 여러번 예약할 수 있다.
  - 둘다 ForeignKey로 연결한다.

- medias

  - 사진 또는 동영상, 그리고 설명
  - Video: Exprience에만 하나씩 들어간다 (OneToOne)

- direct_messages

  - user가 다른 user에게 메시지를 보낸다.
  - blank=True : admin 패널에서는 빈칸으로 표시되지만, db에는 저장된다.
  - Room : 이름이 기존의 Room과 같고, user와 연결되어있으므로, 다른 이름을 사용한다.
  - 2개의 모델이 같은 이름을 가지는 것은 문제가 아니다.

  - django는 \_ 가 있을 경우, 추가로 apps.py의 verbose_name을 변경하여서 복수형을 만들어준다.
