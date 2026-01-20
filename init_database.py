from sqlalchemy.ext.asyncio import AsyncSession

from models import Building, Organization, Practice
from repository import get_objects_count


async def is_db_data_present(session: AsyncSession) -> bool:
    return bool(await get_objects_count(session, Organization))


async def populate_db(session: AsyncSession) -> None:
    # ------------- BUILDINGS -------------
    buildings = [
        Building(
            address="г. Москва, ул. Трубная 15",
            coordinates="55.769372,37.624849",
        ),
        Building(
            address="г. Москва, пер. Пушкарёв 16",
            coordinates="55.768624,37.628458",
        ),
        Building(
            address="г. Москва, ул. Большая Никитская 24/1с5",
            coordinates="55.757480,37.602280",
        ),
        Building(
            address="г. Москва, пер. Вознесенский 7",
            coordinates="55.757859,37.604078",
        ),
        Building(
            address="г. Москва, пер. Последний 15",
            coordinates="55.770144,37.628240",
        ),
    ]

    session.add_all(buildings)
    await session.flush()

    # ------------- PRACTICES -------------
    food = Practice(name="Еда")
    groceries = Practice(name="Продукты", parent=food)
    cafe = Practice(name="Кафе", parent=food)
    bar = Practice(name="Бар", parent=food)
    hookah_lounge = Practice(name="Кальянная", parent=bar)
    mexican = Practice(name="Мексиканская кухня", parent=cafe)
    italian = Practice(name="Итальянская кухня", parent=cafe)
    japanese = Practice(name="Японская кухня", parent=cafe)

    housing = Practice(name="Жилье")
    hotel = Practice(name="Отель", parent=housing)
    mini_hotel = Practice(name="Мини-отель", parent=hotel)
    aparthotel = Practice(name="Апартотель", parent=hotel)

    finance = Practice(name="Финансы")
    financial_consulting = Practice(name="Финансовый консалтинг", parent=finance)
    banking = Practice(name="Банковские услуги", parent=finance)
    atm_machine = Practice(name="Банкомат", parent=banking)
    money_transfers = Practice(name="Денежные переводы", parent=banking)

    practices = [
        food,
        groceries,
        cafe,
        bar,
        hookah_lounge,
        mexican,
        italian,
        japanese,
        housing,
        hotel,
        mini_hotel,
        aparthotel,
        finance,
        financial_consulting,
        banking,
        atm_machine,
        money_transfers,
    ]

    session.add_all(practices)
    await session.flush()

    # ------------- ORGANIZATIONS -------------
    organizations = [
        Organization(
            name="Эль Боррачо",
            phone_numbers=["8-909-634-15-15"],
            building_id=buildings[0].id,
            practices=[bar, mexican]
        ),
        Organization(
            name="Мария Санта",
            phone_numbers=["8-919-764-44-40", "8-919-725-22-88"],
            building_id=buildings[0].id,
            practices=[italian]
        ),
        Organization(
            name="Seven Hills",
            phone_numbers=["8-926-773-67-07", "8-499-503-66-77"],
            building_id=buildings[0].id,
            practices=[mini_hotel]
        ),
        Organization(
            name="Банкомат Сбербанк",
            phone_numbers=[],
            building_id=buildings[0].id,
            practices=[atm_machine]
        ),
        Organization(
            name="Мини-отель на Пушкарёвом 16",
            phone_numbers=["8-909-970-22-44"],
            building_id=buildings[1].id,
            practices=[mini_hotel, aparthotel]
        ),
        Organization(
            name="Dukh",
            phone_numbers=["8-917-262-95-95"],
            building_id=buildings[2].id,
            practices=[cafe, hookah_lounge]
        ),
        Organization(
            name="Национальное бюро кредитных историй",
            phone_numbers=["8-495-221-78-37", "8-800-600-64-04"],
            building_id=buildings[2].id,
            practices=[financial_consulting]
        ),
        Organization(
            name="Банкомат ВТБ",
            phone_numbers=[],
            building_id=buildings[3].id,
            practices=[atm_machine]
        ),
        Organization(
            name="Золотая Корона",
            phone_numbers=["8-495-960-05-55"],
            building_id=buildings[3].id,
            practices=[money_transfers]
        ),
    ]

    session.add_all(organizations)

    await session.commit()
