# coding=utf-8
import numpy
import xlrd
import xlwt
import os
if __name__ == '__main__':
    bumen={
  "高速":"张林",
  "大数据":"刘国宏",
  "一部":"姜林青 ",
  "二部":"许彦良",
  "三部":"陈帅"
}

    names={
        '宋贤贤': 883256,
        '何飞虎': 883244,
        '孙赵龙': 883257,

        '陶洁': 883181,
        '吴留敏': 883212,

        '谭明成': 883249,
        '张熙': 883263,


        '关明哲': 883258,
        '魏健': 883261,
        '刘海飞': 883205,
        '刘鑫宇': 883204,

        '梁有琦': 883199,
        '张家博': 883272,
        '邹江':'无',
        '薛淇文':'无',
    '冷静':883270,
    '李佳玉':883266,
    '蔡啸新':883252,
    }
    # 10-11月    2020-12月产业链工作量核算
    dir='C:\\Users\wu_lmin\Desktop\新建文件夹\\10-11月'
    dir_=dir+"_"
    if  not os.path.isdir(dir_):
        os.mkdir(dir_)
    for filename  in os.listdir(dir):
        print(filename)
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            book = xlrd.open_workbook(dir+"/" + filename)
            sheetname=book.sheets()[0].name

            sheet = book.sheet_by_name(sheetname)
            rows = []
            for i in range(sheet.nrows):
                row = sheet.row_values(i)
                rows.append(row)
            rows[0][0] = filename.split("-")[1].split("月")[0] + "月开发"
            rows[1] = ['事业部', '对应事业部项目的项目名称', '对应事业部项目编号', '项目经理姓名', '人员姓名', '员工号', '开始时间', '结束时间', '实际工作日天数',
                       '当月工作日总数',
                       '人月单价', '结算金额', '职级认定', '备注']
            for r in rows[2:]:
                if r[0] == '':
                    rows.remove(r)
                    continue

                if r[1] == '':
                    r.insert(5, '')
                    r.insert(6, '')
                    if len(r) <= 14:
                        r.extend(numpy.array([''] * (14 - len(r))))
                    continue
                    #     学号
                r.insert(5, names.get(r[4]))
                print(r[6])
                temp=r[6].split('-')
                if len(temp)==1:
                    temp = r[6].split('－')
                print(temp)
                startTime = temp[0].replace('.', '-')
                endTime = temp[1].replace('.', '-')
                r.insert(6, startTime)
                r[7] = endTime
                # 职级认定
                # 备注
                if len(r) <= 14:
                    r.extend(numpy.array([''] * (14 - len(r))))

                pass
            rows = rows[:-2]
            rows.append(['', '', '', '', '', '', '', '', '甲方：山东中创软件' + rows[2][0]])

            rows.append(['', '', '', '', '', '', '', '', '负责人'])
            rows.append(['', '', '', '', '', '', '', '', '乙方：昆山中创软件开发部'])
            rows.append(['', '', '', '', '', '', '', '', '地址：'])
            rows.append(['', '', '', '', '', '', '', '', '联系人：刘志勇'])
            rows.append(['', '', '', '', '', '', '', '', '联系电话：'])
            #
            for r in rows:
                print(r)
            result = xlwt.Workbook()
            sh = result.add_sheet(sheetname)
            for i in range(len(rows)):
                for j in range(len(rows[i])):
                    sh.write(i, j, label=rows[i][j])
            # if filename.endswith("xlsx"):
            #     filename=filename[:-1]
            result.save(dir_+"/"+filename)



    # # sheet.put_cell(1, 1, 1, "test", 0)
    # print(sheet.row(0))
    # # for i in range(sheet.nrows):
    # #     row = sheet.row_values(i)
    # #     print(i, row)
    # #     count += 1
    # test=openpyxl.open('C:\\Users\wu\Documents\Tencent Files\\3200456059\FileRecv\产业链\产业链\\6-9产业链核算/2020-6至9月产业链工作量核算（金二）.xlsx')
    # fd=test.get_sheet_by_name('金融二部')
    # gf=openpyxl.Workbook().active

    # print(fd['A1'])