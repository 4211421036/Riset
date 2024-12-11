using System;
using System.IO.Ports;
using System.Net.Http;
using System.Threading.Tasks;
using System.Timers;

public class Program
{
    private static SerialPort serialPort;
    private static HttpClient httpClient = new HttpClient();
    private static Timer timer;
    private static string wifiSSID = "Galaxy";
    private static string wifiPassword = "fkhw8785";
    private static string botToken = "7060753004:AAGewXhhGtqohZws0WXAKQ-QrJORKy0lAhU";
    private static string chatId = "-1002151631955";
    private static int heaterPin = 21;
    private static int fanPin = 17;
    private static int soilMoisturePin = 0;
    private static float soilPH = 7.0f;

    public static async Task Main(string[] args)
    {
        serialPort = new SerialPort("COM3", 115200);
        serialPort.Open();

        timer = new Timer(1000);
        timer.Elapsed += async (sender, e) => await Loop();
        timer.Start();

        Console.WriteLine("Connecting to WiFi...");
        // Simulate WiFi connection
        await Task.Delay(5000);
        Console.WriteLine("Connected to WiFi");

        await SendMessage("Bot telah diaktifkan dan siap menerima perintah. Ketik /start untuk melihat perintah yang tersedia.");
    }

    private static async Task Loop()
    {
        int soilMoistureValue = ReadSoilMoisture();
        Console.WriteLine($"Soil Moisture Value: {soilMoistureValue}");

        string soilCondition = DetermineSoilCondition(soilMoistureValue);
        Console.WriteLine($"Soil Condition: {soilCondition}");
        Console.WriteLine($"Adjusted Soil pH: {soilPH}");

        float temperature = ReadTemperature();
        if (float.IsNaN(temperature))
        {
            Console.WriteLine("Failed to read from DHT sensor!");
            return;
        }

        Console.WriteLine($"Temperature: {temperature}°C");

        if (temperature < 40.0)
        {
            // Turn on heater
            Console.WriteLine("Suhu terlalu rendah! Pemanas dinyalakan.");
            await SendMessage("Suhu terlalu rendah! Pemanas dinyalakan.");
        }
        else
        {
            // Turn off heater
            Console.WriteLine("Suhu cukup hangat. Pemanas dimatikan.");
            await SendMessage("Suhu cukup hangat. Pemanas dimatikan.");
        }

        // Check for messages from bot
        await CheckMessages();
    }

    private static int ReadSoilMoisture()
    {
        // Simulate reading soil moisture
        return new Random().Next(0, 1023);
    }

    private static string DetermineSoilCondition(int soilMoistureValue)
    {
        if (soilMoistureValue < 300)
        {
            soilPH += 0.5f;
            return "Dry";
        }
        else if (soilMoistureValue >= 300 && soilMoistureValue < 700)
        {
            return "Moist";
        }
        else
        {
            soilPH -= 0.5f;
            return "Wet";
        }
    }

    private static float ReadTemperature()
    {
        // Simulate reading temperature
        return new Random().Next(20, 50);
    }

    private static async Task SendMessage(string message)
    {
        var response = await httpClient.GetAsync($"https://api.telegram.org/bot{botToken}/sendMessage?chat_id={chatId}&text={message}");
        response.EnsureSuccessStatusCode();
    }

    private static async Task CheckMessages()
    {
        var response = await httpClient.GetAsync($"https://api.telegram.org/bot{botToken}/getUpdates");
        response.EnsureSuccessStatusCode();
        var content = await response.Content.ReadAsStringAsync();
        Console.WriteLine(content);
    }
}
