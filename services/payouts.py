from DB.payouts import get_worker_salary

async def get_user_calculation(section_id:int, user_id: int) -> float | None:
    total = await get_worker_salary(section_id, user_id)
    if total == 0:
        return None
    return total

