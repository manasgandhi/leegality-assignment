import factory

from network.models import RouteQuery


class RouteQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RouteQuery

    source = factory.Sequence(lambda n: f"Source{n}")
    destination = factory.Sequence(lambda n: f"Destination{n}")
    total_latency = factory.Faker("pyfloat", min_value=1, max_value=100, right_digits=1)
    path = factory.LazyAttribute(lambda o: [o.source, o.destination])
