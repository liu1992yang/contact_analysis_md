import sys
import re

FILTER = 4

def read_label(labelFile):
  print('reading label file')
  with open(labelFile, "r") as fin :
    blocks = fin.read().splitlines()
    block_label = {}
    for line in blocks:
      block = line.split(':')[0]
      labels = line.split(':')[1].split(',')
      block_label.setdefault(block,labels)
    return block_label

def get_center(block_label):
  for v in block_label.values():
    pair=list(v)[0]
    common=pair.split('-')[0]
    return common


def read_log_filter(datalog, common):
  print("Reading data file")
  with open(datalog, "r") as fin:
    col_sum_dict = {}
    listCounts = []
    for line in fin:
      if line.startswith(" "):
        continue
      if line.startswith(common):
        colNames = line.strip().split()
        
        print("Got " + str(len(colNames)) + " columns!")
        continue
      else :
        numbers = line.strip().split()
        if len(numbers) == 0:
          break
        dists = list(map(float, numbers))
        counts = list(map(lambda x: x <= FILTER, dists))
        listCounts.append(counts)
    step_contact_bool = list(map(max, listCounts))
    count_col = list(zip(*listCounts)) #*sign to unpack nested list/tuple
    sum_col = list(map(sum, count_col))
    #print(step_contact_bool)
    for i in range(len(colNames)):
      col_sum_dict[colNames[i]] = sum_col[i]
    return col_sum_dict, step_contact_bool


def total_contact_steps(step_contact_bool):
  return sum(step_contact_bool)


def sum_by_residue(block_label, col_sum_dict):
  block_sum={}
  label_sum = 0
  for block, labels in block_label.items():
    label_sum = sum([col_sum_dict[label] for label in labels])
    block_sum.setdefault(block, label_sum)
  return block_sum


def by_ratio(block_sum):
  block_fraction = {}
  print(list(block_sum.values()))
  sum_all_block = sum(list(block_sum.values()))
  print('sum = {}'.format(str(sum_all_block)))
  if sum_all_block == 0:
    return block_sum, sum_all_block
  for block, count in block_sum.items():
    block_fraction[block]=count/sum_all_block
  return block_fraction, sum_all_block

###TEMP WRITE OUT STYLE
def write_out_flat(block_fraction,sum_all_block,contact_steps, output):
  with open(output, 'w') as fout:
    fout.write('\t'.join(block_fraction.keys())+'\tTOTAL\tCONTACT_STEPS\n')
    fout.write('\t'.join(list(map(lambda x: "{0:.3f}".format(x), block_fraction.values()))+[str(sum_all_block),str(contact_steps)]) +'\n')

if __name__ == '__main__':
  if len(sys.argv) < 4:
    print("python count_blocks_md.py label_by_block.txt datalog output.txt")
    sys.exit()
  labelFile = sys.argv[1] 
  datalog = sys.argv[2]
  output = sys.argv[3]
  filter_str = str(FILTER).replace('.','p')
  fout_name = output.split('.')[0]+ '_' + filter_str + '.txt'
  block_label = read_label(labelFile)
  center = get_center(block_label)
  col_sum_dict, step_contact_bool = read_log_filter(datalog, center)
  block_sum=sum_by_residue(block_label, col_sum_dict) #total cout
  block_frac, sum_all_block = by_ratio(block_sum)
  contact_steps = total_contact_steps(step_contact_bool)
  #print('contact_steps = {}'.format(str(contact_steps)))
  write_out_flat(block_frac, sum_all_block, contact_steps, fout_name) 









