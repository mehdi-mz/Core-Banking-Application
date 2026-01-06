from functools import wraps
from datetime import datetime
from time import time
from pymssql import connect



def PerformanceLogger(main_function):

    @wraps(main_function)
    def wrapper(*args,**kwargs):

        function_name = main_function.__name__
        call_datetime = datetime.now()

        start_function = time()
        result = main_function(*args,**kwargs)
        stop_function = time()
        exection_time = stop_function-start_function

        with connect(host=".", database="Bank Management Application") as connection:
            cursor = connection.cursor()
            cursor.execute("""
                        insert PerformanceLogger(FunctionName,CallDateTime,ExecutionTime)
                        values (%s,%s,%d)""",(function_name,call_datetime,exection_time))
            connection.commit()

        return result
    return wrapper