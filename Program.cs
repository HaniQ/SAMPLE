using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace ConsoleApplication2
{ 
    
    class TextFile
    {

        static public string CheckTextFile()
        {
            string text = System.IO.File.ReadAllText(@"C:\Users\hani\OneDrive\Documents\Fourth Year\SAVED\TestFolder\WriteLines.txt");
            System.Console.WriteLine("Instruction = {0}", text);
            return text;
        }

        static public void WriteToTextFile()
        {
            string text1 = "Start";
            System.IO.File.WriteAllText(@"C:\Users\hani\OneDrive\Documents\Fourth Year\SAVED\TestFolder\WriteLines.txt", text1);
            Console.WriteLine(text1);
        }

        static void Main()
        {

            int StartPhotos = 0;
            while (true)
            {
                string text = CheckTextFile().ToUpper(); //Check what the top line in the designated text file is 
                Console.WriteLine(text); // Print onto the console what it is 
            if (text == "READY") // If it is READY then proceed with this loop 
                {
                    do
                    {
                        for (StartPhotos = 0; StartPhotos < 5; StartPhotos++) //Iteration loop 
                        {
                            Console.WriteLine("Taking photo with current settings..."); //Print that the caemera is taking photos 
                            Thread.Sleep(2000); //
                        }
                    } while (StartPhotos < 5);

                WriteToTextFile();
                }

            else
                {
                Console.WriteLine("It's not worked... Why not?");
                Thread.Sleep(3000);

                }
            }
            }
        }
    }

