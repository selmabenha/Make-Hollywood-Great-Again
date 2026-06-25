# read file and assign lines as list to variable stacktest_dict
#   stripping line feed from each line
import re
import subprocess

def change_number_in_file(file_to_modify, line_to_modify, part_to_replace, number):
    spider_list = []
    with open(file_to_modify) as spider:
        for line in spider.readlines():
            spider_list.append(re.split(r'(\s)', line))
            #print(line)

    new_s = part_to_replace + str(number)
    # replace string in chosen line with new string
    for line in spider_list:
        #print(line)
        for i in line:
            #print(i)
            if i == line_to_modify:
                print("YES")
                index = line.index(i)
                previous = number - 1
                i = i.replace(part_to_replace + str(previous), new_s)
                line[index] = i

    # write lines with linefeeds added back to file
    #  using an f-string
    with open(file_to_modify, 'w') as spider:
        for line in spider_list:
            spider.writelines([f"{i}" for i in line])

def main():

    ## LOLO SETTINGS
    start = 2
    end = 5

    proc = subprocess.Popen('scrapy crawl mojo -L WARN')
    proc.wait()

    
    for k in range(start, end, 1):
        number = k+1
        file_to_modify = 'mojo/spiders/boxoffice_spider.py'
        line_to_modify = "pd.read_csv('batch/megaset-batch-" + str(number-1) + ".csv')"
        part_to_change = 'megaset-batch-'
        change_number_in_file(file_to_modify, line_to_modify, part_to_change, number)

        file_to_modify = 'mojo/pipelines.py'
        line_to_modify = 'csv.writer(open("batch' + str(number-1) + '.csv",'
        part_to_change = 'batch'
        change_number_in_file(file_to_modify, line_to_modify, part_to_change, number)

        proc = subprocess.Popen('scrapy crawl mojo -L WARN')
        proc.wait()
    
if __name__ == '__main__':
    main()