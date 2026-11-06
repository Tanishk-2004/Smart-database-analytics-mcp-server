# Testing File.

from database.query_executer import execute_query


def main(): 
    query="Select full_name,city from customers limit 1 "

    results=execute_query(query)

    for row in results:
        print(row["full_name"])
        print(row["city"])
        print("----------------")

if __name__=="__main__":
    main()