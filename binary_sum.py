def comp_1(nums):
  
  nums_inv = ''

  for i in range(0, len(nums)):
  
    if nums[i] == '0':
      nums_inv += '1'
  
    else:
      nums_inv += '0'

  return nums_inv

def adder_1_bit(a, b=None, c_in=0, op=0):
  
  if b is None:
    b = 0
  
  # If op is 0, so sum
  b = op ^ b
  a_b = a ^ b
  
  r_sum = a_b ^ c_in

  and_01 = a & b
  and_02 = b & c_in
  and_03 = a & c_in

  r_c_out = and_01 | and_02 | and_03

  return r_sum, r_c_out

# To negative
def comp_2(nums):
  
  aux = 0
  res = ""
  
  print("Original........:", nums)
  print("1's complement..:", comp_1(nums))
  print("................:   +1")
  print("-"*25)

  for i in comp_1(nums)[::-1]:
    if aux < 1:
      aux += 1
      ret = adder_1_bit(int(i), b=1)
      res += str(ret[0])
      continue
    
    ret = adder_1_bit(int(i), c_in=ret[1])
    res += str(ret[0])

  return res[::-1]
  
def full_adder(a, b):
  
  res = ""
  c_out = 0

  for i, j in zip(a[::-1], b[::-1]):
    
    ret = adder_1_bit(int(i), int(j), c_in=c_out)

    res += str(ret[0])
    c_out = ret[1]

  print(res[::-1])
  return res[::-1]

if __name__ == "__main__":
  # Subtracting
  print("1" + comp_2(full_adder("0011", comp_2("0100"))[1:]) )

  # Adding
  # full_adder("0011", "0001")
  
  # Representation of negative numbers
  # print("Ret",comp_2("111"))