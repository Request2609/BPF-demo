#!/usr/bin/python
#encoding: utf-8

# 删除   delete from add_test where time>=1564150279123000000
# 查询   select * from thread_create_count

def query_ql(table, cond):
    return "select "+cond+"  from "+ table

def delete_ql(table, cond):
    return "delete from "+ table+"  where "+cond