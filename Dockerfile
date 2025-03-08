# Use an official Ubuntu image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    git \
    cmake \
    libboost-all-dev \
    libasio-dev \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip3 install torch torchvision pillow transformers  --break-system-packages

RUN git clone https://github.com/CrowCpp/Crow.git && \
    cd Crow && mkdir build && cd build && \
    cmake .. && make -j$(nproc) && make install && \
    cd ../.. && rm -rf Crow

# Set working directory
WORKDIR /app

# Copy source code
COPY server.cpp .
COPY embed_image.py .

# Compile the C++ Crow server
RUN g++ -o server server.cpp -lboost_system -lpthread

# Expose port 8080
EXPOSE 8080

# Run the server
CMD ["./server"]
