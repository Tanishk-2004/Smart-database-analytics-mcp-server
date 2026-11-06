from database.db_connection import get_connection


def main():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("Select count(*) From customers")

                rows=cur.fetchall()

                for row in rows:
                    print(row)

            print("Database connection successfull!")
    except Exception as e:
        print("Something went wrong:",e)


if __name__=="__main__":
    main()