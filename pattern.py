# a = "Rakesh"
# for i in range(0,6):
#     print(a[i],"", end="")
    
# for i in range(0,5):
#     for j in range(0,i+1):
#         print("*", end="")
#     print()

# for i in range(1,6):
#     for j in range(0,i+1):
#         print(j, end="")
#     print()

# for i in range(1,6):
#     for j in range(1,i+1):
#         print(i, end="")
#     print()
    
    
# for i in range(0,5):
#     for j in range(0,i+1):
#         print(j+1, end="")
#     print()
    
# for i in range(0,5):
#     for j in range(0,i+1):
#         print(i+1, end="")
#     print()

# for i in range(0,5):
#     for j in range(0,5-i):
#         print("j", end="")
#     print()

# a = "Rakesh"
# b = "Rahul"
# for i in range(0,6):
#     print (a[i])
#     for j in range(0,5):
#         print(b[j])

# # wrong code range never goes backwards in python, so the below code will not work
# for i in range(7,1):
#     for j in range(1,7-i):
#         print(i, end="")
#     print()


# for i in range(7,1,-1):
#     for j in range(1,7-i):
#         print(i, end="")
#     print()
    
# for i in range(5, 0, -1):
#     for j in range(i):
#         print("*", end="")
#     print()
    
# for i in range(5):
#     for j in range(i):
#         print(" ", end="")
#     for j in range(5 - i):
#         print("*", end="")
#     print()

# for i in range(5, 0, -1):
#     print(" " * (5 - i), end="")
#     for j in range(1, i + 1):
#         print(j, end="")
#     print()
    
 
# for i in range(5, 0, -1):
#     for j in range(5 - i):
#         print(" ", end="")
#     for j in range(i):
#         print(i, end="")
#     print()

# # pyramid pattern
# n = 5
# for i in range(1, n + 1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
    
# # reverse pyramid pattern
# n= 5 
# for i in range(n, 0, -1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
    
# # diamond pattern  
# n = 5
# for i in range(1, n + 1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
# for i in range(n - 1, 0, -1):
#     for j in range(n - i):
#         print(" ", end="")
#     for j in range(2 * i - 1):
#         print("*", end="")
#     print()
    
# output
#    *
#    ***
#   *****
#  *******
# *********
#  *******
#   *****
#    ***
#     *


# x=5
# for i in range(1,6):
#     for k in range(1,x+1):
#         print(" ", end="")
#     for j in range(1,i+1):
#         print("*", end="")
#     print()
#     x=x-1
    
# output
#      *
#     **
#    ***
#   ****
#  *****

# x=5
# for i in range(5,0,-1):
#     for k in range(1,x+1):
#         print(" ", end="")
#     for j in range(1,i+1):
#         print("*", end="")
#     print()
#     x=x-1