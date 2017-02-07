using System;
using System.Collections.Generic;
using System.Threading;
using EDSDKLib;
using System.Linq;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.IO;

namespace ConsoleExample
{
    class Program
    {
        static SDKHandler CameraHandler;
        static bool WaitForEvent;

        static public string CheckTextFile()
        {
            string text = System.IO.File.ReadAllText(@"C:\Users\hani\OneDrive\Documents\Fourth Year\SAVED\TestFolder\WriteLines.txt");
            System.Console.WriteLine("Instruction = {0}", text);
            return text;
        }

        static public void StartBuggy()
        {
            string text1 = "Start";
            System.IO.File.WriteAllText(@"C:\Users\hani\OneDrive\Documents\Fourth Year\SAVED\TestFolder\WriteLines.txt", text1);
            Console.WriteLine(text1);
        }

        static void Main(string[] args)
        {
            try
            {
                CameraHandler = new SDKHandler();
                CameraHandler.SDKObjectEvent += handler_SDKObjectEvent;
                List<Camera> cameras = CameraHandler.GetCameraList();
                if (cameras.Count > 0)
                {
                    CameraHandler.OpenSession(cameras[0]);
                    Console.WriteLine("Opened session with camera: " + cameras[0].Info.szDeviceDescription);
                }
                else
                {
                    Console.WriteLine("No camera found. Please plug in camera");
                    CameraHandler.CameraAdded += handler_CameraAdded;
                    CallEvent();
                }

                int StartPhotos = 0;
                while (true)
                {
                    string text = CheckTextFile().ToLower();
                    if (text == "ready")
                    {
                        do
                        {
                            for (StartPhotos = 0; StartPhotos < 5; StartPhotos++)
                            {
                                Console.WriteLine("Taking photo with current settings...");
                                CameraHandler.SetCapacity();
                                CameraHandler.TakePhoto();
                                Thread.Sleep(2000);
                            }
                        } while (StartPhotos < 5);
                        StartBuggy();
                    }

                    else
                    {
                        Thread.Sleep(2000);
                        Console.WriteLine("I have stopped checking now");
                    }

                    CallEvent();
                    Console.WriteLine("Photo taken and saved");
                }
            }
            catch (Exception ex) { Console.WriteLine("Error: " + ex.Message); }
            finally
            {
                CameraHandler.CloseSession();
                CameraHandler.Dispose();
                Console.WriteLine("Good bye! (press any key to close)");
                Console.ReadKey();
            }
        
        }

        static void CallEvent()
        {
            WaitForEvent = true;
            while (WaitForEvent)
            {
                EDSDK.EdsGetEvent();
                Thread.Sleep(200);
                string text = CheckTextFile().ToLower();
                if (text == "ready")
                {
                    WaitForEvent = false; 
                }
            }
        }

        static uint handler_SDKObjectEvent(uint inEvent, IntPtr inRef, IntPtr inContext)
        {
            if (inEvent == EDSDK.ObjectEvent_DirItemRequestTransfer || inEvent == EDSDK.ObjectEvent_DirItemCreated) WaitForEvent = false;
            return EDSDK.EDS_ERR_OK;
        }

        static void handler_CameraAdded()
        {
            List<Camera> cameras = CameraHandler.GetCameraList();
            if (cameras.Count > 0) CameraHandler.OpenSession(cameras[0]);
            Console.WriteLine("Opened session with camera: " + cameras[0].Info.szDeviceDescription);
            WaitForEvent = false;
        }
    }
}
