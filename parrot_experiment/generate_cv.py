def generate_cv(elt_list, start, reps):
	index = 0
	for i in range(start,start+reps*len(elt_list)):
		i_string = str(i)
		while len(i_string) < 3:
			i_string = "0" + i_string
		elt = elt_list[index]
		
		elt_copy = elt.replace("#",i_string)

		print elt_copy
		
		if index == len(elt_list) - 1:
			index = 0
		else:
			index+=1

test_list = ["A,#,https://testurl.com/a","B,#,https://testurl.com/b","C,#,https://testurl.com/c"]

generate_cv(test_list, 1, 15)