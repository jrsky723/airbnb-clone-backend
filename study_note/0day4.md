# DAY 4

### 10.8 DELETE

- 웹페이지의 api기능을 구현한 페이지의 주소는 /api/v1/~ 과 같이 정해준다.

### 10.9 Recap

- django serializer는 django object를 json으로 바꿔준다.
- room model에서 serializer를 만들때 코드 겹침이 많다.

### 10.11 ModelSerializer

- ModelSerializer에는 default로 create, update가 있다.
  - model로 부터 serializer를 만들때는, ModelSerializer를 사용하자.
- field or exclude를 사용해서, 원하는 field만 보내거나, 원하지 않는 field를 보내지 않을 수 있다.

- model serializer의 내부에서 어떤 작업들이 이루어지는지 알 필요가 있다.
  - create, update, validation 등등

### 10.12 ModelViewSet

- ModelViewSet

  - list, create, retrieve, update, partial_update, destroy 지원
  - queryset, serializer_class 지정
  - get_queryset, get_serializer_class를 오버라이딩해서 사용할 수 있다.

- ModelViewSet을 사용하면, 코드가 간결해진다.
- HTTP method와 ModelViewSet의 method를 매핑해준다.

### Conclusion

- 추가적인 기능들 (documentation을 참고 할 것)

  - Router를 사용해서 url을 자동으로 생성해주는 기능
  - ReadonlyModelViewSet
    - list, retrieve만 지원
  - mixins
    - 사용자 정의 viewset을 만들때 사용
  - viewset을 사용하는 것은 추상화를 통해서 코드를 간결하게 만드는 것이다.

    - but, 직접 view를 만드는 것이 explicit하다.
    - 예를 들어, 직접 view를 설정할때, category를 지우기 전에 email을 보내야 한다면, viewset을 사용하기 어렵다.
    - destroy method를 오버라이딩해서 사용해야 한다.
    - 만약 사용자가 소유하고 있는 category만 retrieve할 수 있게 하고 싶다면, get_queryset을 오버라이딩해서 사용해야 한다.
    - 이러한 사소한 기능들 때문에, ViewSet을 costumize하기 어렵다.
    - 그럴바엔, APIView를 사용하는 것이 낫다.

  - delete, create, retireve, list만 구현한다면, ViewSet을 사용하는 것이 좋다.
  - 그 외의 기능들은 APIView를 사용하는 것이 좋다.
  - 사용자가 이메일 인증을 했는지 안했는지에 따라서, 다른 기능을 구현하고 싶다면, APIView를 사용하는 것이 좋다.
  - explicit is better than implicit
  - 나중에 내 코드를 본다면, 내가 무슨 기능을 구현하고 싶었는지 알 수 있어야 한다.
