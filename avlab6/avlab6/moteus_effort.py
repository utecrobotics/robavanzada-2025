import asyncio
import math
import moteus

MASS_Kg = 0.0  # Mass of the Link (Kg)
LENGTH_m = 0.0 # Length of the link (m)
RATE_Hz = 50    # Rate control loop (Hz)

async def main():

  transport = moteus.Fdcanusb()

  pr = moteus.PositionResolution()
  pr.position = moteus.IGNORE
  pr.velocity = moteus.IGNORE
  pr.feedforward_torque = moteus.F32
  pr.kp_scale = moteus.INT8
  pr.kd_scale = moteus.INT8

  controller = moteus.Controller(id = 1, position_resolution = pr)

  await transport.cycle([controller.make_stop()])

  missed_replies = 0
  ff_torque = 0

  print("Starting control loop ...")

  try:
    while True:
      result = await transport.cycle([controller.make_position(feedforward_torque=ff_torque, kp_scale=0.0, kd_scale=0.0, query=True)])
            
      if len(result) == 0:
        missed_replies += 1
        if missed_replies > 3:
          print("MOTOR TIMEOUT!")
          await transport.cycle([controller.make_stop()])
          print("The mjbots node is close!")
          sys.exit()
        continue
      else:
        missed_replies = 0

      data = result[0]
      mode = data.values[moteus.Register.MODE]
      position = data.values[moteus.Register.POSITION]
      torque = data.values[moteus.Register.TORQUE]
      temperature = data.values[moteus.Register.TEMPERATURE]

      ff_torque = 0

      print(f"Mode: {mode}, Position: {position}, cmd_torque: {ff_torque}, temperature: {temperature}")

      await asyncio.sleep(1/RATE_Hz)
                
  except KeyboardInterrupt:
    print("The mjbots node is closed!")
  finally:
    await transport.cycle([moteus_controller.make_stop()])
    print("Exiting the program.")
    sys.exit()
    
if __name__ == '__main__':
  asyncio.run(main())
