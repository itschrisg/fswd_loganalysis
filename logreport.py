#!/usr/bin/env python3
#
# A command-line solution to produce a report from the
# website log database
#

import psycopg2

db_name = "news"
q1_sql = "select * from v_articleviewstats order by view_count desc limit 3"
q2_sql = "select	* from v_authorviewstats order by view_count desc"
q3_sql = "select * from v_errorstats"

try:
    db = psycopg2.connect(database=db_name)
    qc = db.cursor()
except psycopg2.Error as err:
    print "Unable to connect"
    print err.pgerror
    print err.diag.message_detail
    sys.exit(1)
else:
    
    # Execute the first query - get the top 3 viewed articles
    qc.execute(q1_sql)
    articleViewStats = qc.fetchall()
    print('\n\n1. The Three Most Popular Articles of all time\n')

    for record in articleViewStats:
        print('   * {} - {} views'.format(record[0], record[1]))

    # Execute the second query - get the most popular article authors of all time
    qc.execute(q2_sql)
    authorStats = qc.fetchall()
    print('\n\n2. Author Popularity - ranked from most popular to least popular\n')

    for record in authorStats:
        print('   * {} - {} views'.format(record[0], record[1]))

    # Execute the second query - get the most popular article authors of all time
    qc.execute(q3_sql)
    errorStats = qc.fetchall()
    print('\n\n3. Website Error Statistics - days exceeding 1% errors\n')

    for record in errorStats:
        fdate = record[0].strftime('%B %d, %Y')
        print('   * {} - {} error rate'.format(fdate, record[1]))

    print('\n\n')
    db.close()
