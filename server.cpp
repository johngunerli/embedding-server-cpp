#include <cstdlib>
#include <fstream>
#include <sstream>
#include <iostream>
#include "crow.h"

std::string runPythonScript(const std::string& jsonPath) {
    std::string command = "python3 embed_image.py " + jsonPath;
    std::string result;
    char buffer[128];

    FILE* pipe = popen(command.c_str(), "r");
    if (!pipe) return "Error executing Python script";

    while (fgets(buffer, sizeof(buffer), pipe) != nullptr) {
        result += buffer;
    }
    pclose(pipe);

    // Print to console
    std::cout << "Python script output: " << result << std::endl;

    return result;
}

int main(int argc, char* argv[]) {
    crow::SimpleApp app;

    CROW_ROUTE(app, "/")([]() {
        return crow::response("Send an image array as JSON to /embed.");
    });

    CROW_ROUTE(app, "/embed").methods(crow::HTTPMethod::POST)([](const crow::request& req) {
        crow::json::rvalue body;
        try {
            body = crow::json::load(req.body);
        } catch (...) {
            return crow::response(400, "Invalid JSON format.");
        }

        if (!body.has("image")) {
            return crow::response(400, "Missing 'image' field in JSON.");
        }

        // Save JSON to a file
        std::string filename = "/tmp/image_data.json";
        std::ofstream file(filename);
        file << req.body;
        file.close();

        // Run the Python script to process the JSON
        std::string embedding = runPythonScript(filename);

        // Return response to API
        return crow::response(embedding);
    });

    app.port(8080).multithreaded().run();
}
