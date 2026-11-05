from DB.works import get_worker_salary

async def get_user_calculation(user_id: int) -> float | None:
    total = await get_worker_salary(user_id)

    if total == 0:
        return None

    return total