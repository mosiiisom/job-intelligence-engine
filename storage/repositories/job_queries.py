from storage.database import get_connection


def get_all_jobs(limit: int = 100) -> list:

    with get_connection() as conn:
        rows = conn.execute('SELECT * FROM jobs ORDER BY posted_at DESC LIMIT ?', (limit,)).fetchall()


    return [dict(row) for row in rows]

def filter_jobs(
        companies=None,
        locations=None,
        employment_types=None,
        tags=None,
        limit: int = 100,
):

    with get_connection() as conn:

        # we set WHERE 1=1 as no filter ( 1=1 mean true ) and if filters doesn't set we will don't have issue with execution
        query = ["SELECT * FROM jobs WHERE 1=1"]
        params = []

        if companies:
            query.append(f"AND company IN ({','.join(['?']*len(companies))})")
            params.extend(companies)

        if locations:
            query.append(f"AND location IN ({','.join(['?']*len(locations))})")
            params.extend(locations)

        if employment_types:
            query.append(f"AND employment_type IN ({','.join(['?']*len(employment_types))})")
            params.extend(employment_types)

        if tags:
            tag_conditions  = []
            for tag in tags:
                tag_conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")

            query.append(f"AND (" + " OR ".join(tag_conditions) + ")")

        query.append("ORDER BY posted_at DESC LIMIT ?")
        params.append(limit)

        final_query = " ".join(query)
        rows = conn.execute(final_query, params).fetchall()

    return [dict(row) for row in rows]


def search_jobs(keyword: str, limit: int = 100):

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM jobs
            WHERE title LIKE ? 
            OR company LIKE ?
            OR tags LIKE ?
            OR location LIKE ?
            ORDER BY posted_at DESC LIMIT ?""", (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", limit)).fetchall()

    return [dict(row) for row in rows]