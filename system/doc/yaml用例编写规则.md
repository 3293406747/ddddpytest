- 一级关键字：必须包含casename、request，可包含data_path、session、extract、assertion。
其中casename为用例名，request为请求内容，data_path为关联的csv测试数据路径，
session为要是用的session索引，默认使用索引为0的session。

- 二级关键字：request中必须包含url、method关键字，
可包含params、data、json、files、headers关键字，
session必须是整数，
extract中可包含request、response关键字，
assertion中可包含equal、unequal、contain、uncontain关键字，关键字下必须为列表形式，列表中字典必须包含expect、actual关键字;

- 使用变量：${变量名}
- 调用python函数：{{方法名(参数)}}
- yaml关联csv测试数据：存在data_path参数时可使用csv中的列名，${csv中的列名},为csv文件中列名时将会被循环替换为对应的值，生成关联后的用例集。
- extract中request为从请求中提取数据，response为从响应中提取数据。键名为给提取出的内容命名，值的第一个字符为$时为json提取，否则为正则提取。值中","为提取值的索引，不存在时为提取全部值。
- assertion中equal、unequal分别为相等断言和不相等断言，其中的expect为预期值，actual为实际值。可使用extract提取出的内容，也可使用变量及调用python函数。
- assertion中contain、uncontain分别为包含断言和不包含断言，其中的每个值为预期值，可使用extract提取出的内容，也可使用变量及调用python函数。
- 注意：使用变量及调用python函数是必要要加双引号或单引号，否则会报错。
- csv测试数据中同样可以使用变量及调用python函数。