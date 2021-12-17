from esp32 import Partition
import gc


# https://forum.micropython.org/viewtopic.php?f=18&t=7066
class Ota:
  
  SEC_SIZE = 4096
  
  def copyPartition(self):
    currentPartition = Partition(Partition.RUNNING)
    nextPartition = currentPartition.get_next_update()
    buf = bytearray(self.SEC_SIZE)
    for i in range(0, currentPartition.info()[3] // self.SEC_SIZE):
      currentPartition.readblocks(i, buf)
      nextPartition.writeblocks(i, buf)
      print('Block No. ' + str(i) + ' copied')
      gc.collect()
    print('Partition copied')
    nextPartition.set_boot()
