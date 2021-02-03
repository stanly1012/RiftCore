# -*- coding: utf-8 -*-
# @Author: Ruige Lee
# @Date:   2021-02-02 17:06:19
# @Last Modified by:   Ruige Lee
# @Last Modified time: 2021-02-03 15:33:13


import sys
import os
import json
import time

import matplotlib.pyplot as plt

res = os.system("iverilog -W all -o ./build/wave.iverilog  -y ../RiftChip/ -y ../RiftChip/riftCore/ -y ../RiftChip/riftCore/backend  -y ../RiftChip/riftCore/backend/issue  -y ../RiftChip/riftCore/backend/execute  -y ../RiftChip/riftCore/frontend  -y ../RiftChip/element -y ../RiftChip/Soc -y ../RiftChip/Soc/xilinx_IP/axi_Xbar -y ../RiftChip/debug -y ../tb  -I ../tb  -I ../RiftChip/  ../tb/riftChip_DS.v  ")


if ( res == 0 ):
	print ("compile pass!")
else:
	print ("compile Fail!")
	DSReturn = -1
	sys.exit(-1)



res = os.system("vvp -N ./build/wave.iverilog -lxt2")


if (res == 0):
	print("dhrystone PASS!")


	with open("./ci/dhrystone.json","r") as f1:
		benchmark = f1.read()
	bm = (json.loads(benchmark))['message']

	# print(bm)
	time = time.asctime( time.localtime(time.time()) )
	# print(str)


	new = []
	with open("./ci/performance","r") as f2:
		history = f2.readlines()

	for item in history:
		item = item.strip('\n')
		# print ("item = ", item)
		hisjs = json.loads(item)
		new.append(hisjs)




	jsStr = "{ \"benchmark\": " + bm + ",\"time\": \" "+ time + " \" }  "

	js = json.loads(jsStr)

	# print ("js = ", js)
	new.append(js)


	# print (type(new))

	with open("./ci/performance","w") as f3:
		for item in new:
			# print (item)
			f3.write(json.dumps(item)+'\n')


else:

	CIReturn = -1
	print(file, "dhrystone FAIL!!!!!!!!!!")
	sys.exit(-1)


performance = []
for item in new:
	performance.append(item["benchmark"])

# print("performance=", performance)

# print(len(performance))
x1 = range(0, len(performance))


plt.xticks([])
plt.scatter(x1, performance, marker='.', s = 1000//len(performance))

# plt.show()
plt.savefig("./ci/performance.png")
