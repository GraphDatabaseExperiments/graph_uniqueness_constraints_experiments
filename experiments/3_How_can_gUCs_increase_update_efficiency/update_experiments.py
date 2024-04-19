'''
Graph Database experiments on Recommendations dataset

Updates
'''


import random # used to split up departments randomly
import math # math module

import xlsxwriter # writing to excel

from neo4j import GraphDatabase

from datetime import datetime

import time # use for benchmarking code and finding bottlenecks





# databse class
class gdbms_test:


    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def reset(self):
        with self.driver.session() as session:
            session.run("MATCH (m) DETACH DELETE m")

    def execute_query(self, query):
        with self.driver.session() as session:
            session.run(query)

    def execute_query_with_output(self, query):
        with self.driver.session() as session:
            record = session.run(query)
        return record


    def execute_query_with_output_result(self, query):
        with self.driver.session() as session:
            record = session.run(query)
        return [dict(i) for i in record]



####################################################

# performing queries



# getting db_hits

def sum_db_hits(profile):
    return (profile.get("dbHits", 0) + sum(map(sum_db_hits, profile.get("children", []))))


# getting execution time

def sum_time(profile):
    return (profile.get("time", 0) + sum(map(sum_time, profile.get("children", []))))


def show_query_details(database, query):

    
    new_db = database
    
    result = new_db.execute_query_with_output(query)

    summary = result.consume().profile


    return  (sum_db_hits(summary), sum_time(summary))


########################

# write to excel file

def write_to_excel(filename, sheetname, experiment_name, heading: list, content: list):

    # create sheet
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet(sheetname)
    
    # write experiment name
    worksheet.write(0,0, experiment_name)

    
    # write heading (list), give information on variables, etc
    row_start = 2

    for row in range(len(heading)):
            worksheet.write(row_start + row, 0, heading[row])

    # write content (content list of iterables)
    row_start += (2 + len(heading))
    column_start = 0

    for row in range(len(content)):
        for column in range(len(content[row])):
            worksheet.write(row_start + row, column_start + column, content[row][column])

    # close workbook
    workbook.close()



#########################

# main function

def main():

    #local bolt and http port, etc:
    local_bolt = "bolt://localhost:7687"
    local_pw = "Pskav752$api"
    local_user = "neo4j"

    # Initialise DB
    new_db = gdbms_test(local_bolt, local_user, local_pw)

    # Initialise db_hits and time for updates
    db_hits = [[[],[]]]
    times = [[[],[]]]

    average_db_hits = [[[],[]]]
    average_time = [[[],[]]]


    # Experiment setting

    factor = 5 # sclaing factor for node size
 


    # current date and time
    today = datetime.now().strftime("%Y_%m_%d")
    current = datetime.now().strftime("%H_%M_%S")


        
    # perform experiment multiple times



    runs = 20

    outliers = 5


    current_db_hits = 0
    current_time = 0

    ## execute experiment

    ## scale node set

    amount_nodes = 442

    scaling_times = 20

    for scaling in range(scaling_times + 1):

        print(f"{scaling_times + 1 - scaling} more experiments to go....")

        for i in range(amount_nodes*(scaling*factor-1)):

            create_node = "CREATE (ad:Actor:Director{name: 'new_" + str(i) + "', bornIn: 'new_" + str(i) + "'})"
            new_db.execute_query(create_node)

        for i in range(runs):


        # updae without index

            update = "PROFILE MATCH (ad:Actor:Director) WHERE ad.name IS NOT NULL AND ad.bornIn IS NOT NULL AND ad.name = 'Larry David' SET ad.languages = 'English'"
            current_db_hits, current_time = show_query_details(new_db, update)
            db_hits[-1][0].append(current_db_hits)
            times[-1][0].append(current_time)

        

        # create index
            
        create_new_label = "MATCH (ad:Actor:Director) WHERE ad.name IS NOT NULL AND ad.bornIn IS NOT NULL SET ad:ActorAndDirector"
        new_db.execute_query(create_new_label)

        create_index = "CREATE INDEX Actor_And_Director_filtered FOR (ad:ActorAndDirector) ON (ad.name)"
        new_db.execute_query(create_index)

        time.sleep(1) #wait for index to be created

        for i in range(runs):

        # update with index

            update = "PROFILE MATCH (ad:ActorAndDirector) WHERE ad.name IS NOT NULL AND ad.bornIn IS NOT NULL AND ad.name = 'Larry David' SET ad.languages = 'English'"
            current_db_hits, current_time = show_query_details(new_db, update)
            db_hits[-1][1].append(current_db_hits)
            times[-1][1].append(current_time)


        # delete nodes, drop new labe and drop index to restart experiment for bigger scaling factor

        drop_index = "DROP INDEX Actor_And_Director_filtered"
        new_db.execute_query(drop_index)
        
        delete_nodes = "MATCH (ad:ActorAndDirector) WHERE ad.name CONTAINS 'new' DELETE ad"
        new_db.execute_query(delete_nodes)

        remove_label = "MATCH (ad:ActorAndDirector) remove ad:ActorAndDirector"
        new_db.execute_query(remove_label)
        



        db_hits[-1][0] = sorted(db_hits[-1][0])[outliers:-outliers]
        db_hits[-1][1] = sorted(db_hits[-1][1])[outliers:-outliers]
        times[-1][0] = [round(time_of_run / 10000) for time_of_run in sorted(times[-1][0])[outliers:-outliers]]
        times[-1][1] = [round(time_of_run / 10000) for time_of_run in sorted(times[-1][1])[outliers:-outliers]]


        average_db_hits[-1][0].append(round(sum(db_hits[-1][0])/(runs - 2*outliers)))
        average_db_hits[-1][1].append(round(sum(db_hits[-1][1])/(runs - 2*outliers)))
        average_time[-1][0].append(round(sum(times[-1][0])/(runs - 2*outliers)))
        average_time[-1][1].append(round(sum(times[-1][1])/(runs - 2*outliers)))

        if scaling != scaling_times:
            db_hits.append([[],[]])
            times.append([[],[]])
            average_db_hits.append([[],[]])
            average_time.append([[],[]])



    
    # Experiment results

    filename = "Update_results_" + str(factor*scaling) + "_" + str(today) + "---" + str(current) + ".xlsx"
    sheetname = "Experiment"
    experiment_name = f"Recommendations update"

    # can probably be deleted
    experiment_details = []

    print("writing...")
    
    # create content for Excel
    content = [["Update: factors 1 to " + str(factor * scaling) + " in steps of " + str(factor), "",""]]
    for index in range(scaling_times + 1):
        if index == 0:
            content.append([f"Updating original:"])
        else:
            content.append([f"Updating with factor {factor * (index + 1)}:"])
        content.append([""])
        content.append(["Without index"])
        content.append(["DbHits: "] + [str(value) for value in db_hits[index][0]] + [" ", "Average DbHits: "] + [str(average_db_hits[index][0][0])])
        content.append(["Time (in ms*100): "] + [str(value) for value in times[index][0]] + [" ", "Average time (in ms*100): "] + [str(average_time[index][0][0])])
        content.append([""])
        content.append(["With index"])
        content.append(["DbHits: "] + [str(value) for value in db_hits[index][1]] + [" ", "Average DbHits: "] + [str(average_db_hits[index][1][0])])
        content.append(["Time (in ms*100): "] + [str(value) for value in times[index][1]] + [" ", "Average time (in ms*100): "] + [str(average_time[index][1][0])])
        content.append([""])
        content.append([""])

    # writing to file
    write_to_excel(filename, sheetname, experiment_name, experiment_details, content)


    # closing db
    new_db.close()


main()




