# Real-time Agent Performance Dashboard - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                         │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              dashboard.html                                │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐          │  │
│  │  │  Metrics   │  │  Request   │  │   Error    │          │  │
│  │  │  Display   │  │  History   │  │    Log     │          │  │
│  │  └────────────┘  └────────────┘  └────────────┘          │  │
│  │                                                            │  │
│  │  Auto-refresh: 5 seconds                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ API Calls
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│            MCP Server (performance_dashboard_server.py)          │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                           │  │
│  │                                                            │  │
│  │  • get_performance_metrics()                              │  │
│  │  • get_request_history(limit)                             │  │
│  │  • get_error_log(limit)                                   │  │
│  │  • simulate_agent_task(name, duration, should_fail)       │  │
│  │  • reset_performance_metrics()                            │  │
│  │  • get_dashboard_data()                                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                   │
│                              ▼                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              PerformanceMetrics Class                      │  │
│  │                                                            │  │
│  │  Thread-Safe Data Storage:                                │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ Metrics Dictionary:                              │    │  │
│  │  │  - total_requests                                │    │  │
│  │  │  - successful_requests                           │    │  │
│  │  │  - failed_requests                               │    │  │
│  │  │  - response times (min/max/avg)                  │    │  │
│  │  │  - success_rate / error_rate                     │    │  │
│  │  │  - uptime                                        │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ Request History (deque, max 100):                │    │  │
│  │  │  - timestamp                                      │    │  │
│  │  │  - endpoint                                       │    │  │
│  │  │  - response_time                                  │    │  │
│  │  │  - success                                        │    │  │
│  │  │  - error                                          │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ Error Log (deque, max 50):                       │    │  │
│  │  │  - timestamp                                      │    │  │
│  │  │  - endpoint                                       │    │  │
│  │  │  - error_message                                  │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                                                            │  │
│  │  Threading Lock: Ensures concurrent access safety        │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Task Execution Flow
```
Agent Task
    │
    ▼
simulate_agent_task()
    │
    ├─ Start timer
    ├─ Execute task (with optional failure simulation)
    ├─ Stop timer
    │
    ▼
record_request()
    │
    ├─ Lock metrics
    ├─ Update counters
    ├─ Update response times
    ├─ Calculate rates
    ├─ Add to history
    ├─ Add to error log (if failed)
    └─ Unlock metrics
```

### 2. Dashboard Update Flow
```
Browser (dashboard.html)
    │
    ├─ Initial load
    │   └─ Call get_dashboard_data()
    │
    └─ Auto-refresh (every 5s)
        │
        ▼
    get_dashboard_data()
        │
        ├─ get_metrics()
        ├─ get_request_history(10)
        └─ get_error_log(5)
        │
        ▼
    Update UI
        │
        ├─ Update metric cards
        ├─ Update request table
        └─ Update error table
```

## Component Interactions

### Performance Metrics Class
- **Purpose**: Central storage and management of performance data
- **Thread Safety**: Uses `threading.Lock()` for concurrent access
- **Data Structures**:
  - Dictionary for metrics (O(1) access)
  - Deque for histories (O(1) append, automatic size limiting)
- **Key Methods**:
  - `record_request()`: Add new request data
  - `get_metrics()`: Retrieve current metrics
  - `reset_metrics()`: Clear all data

### API Layer
- **Purpose**: Expose metrics data via MCP protocol
- **Error Handling**: Validates all inputs, returns structured responses
- **Response Format**: Consistent JSON with status and data fields
- **Rate Limiting**: Built-in caps on history/log requests

### Web Dashboard
- **Technology**: Pure HTML/CSS/JavaScript (no frameworks)
- **Update Mechanism**: JavaScript auto-refresh using setInterval
- **UI Components**:
  - Metric cards (8 key metrics)
  - Request history table
  - Error log table
  - Control buttons
  - Status indicator

## Concurrency Model

```
Multiple Threads/Requests
    │
    ├─ Thread 1: simulate_agent_task()
    │       │
    │       └─ Acquire Lock ──► Update Metrics ──► Release Lock
    │
    ├─ Thread 2: get_performance_metrics()
    │       │
    │       └─ Acquire Lock ──► Read Metrics ──► Release Lock
    │
    └─ Thread 3: get_request_history()
            │
            └─ Acquire Lock ──► Read History ──► Release Lock
```

## Scalability Considerations

### Current Implementation
- **History Size**: Limited to 100 entries (configurable)
- **Error Log**: Limited to 50 entries (configurable)
- **Memory**: O(n) where n = max history size
- **Thread Safety**: Fine-grained locking

### Performance Characteristics
- **Metric Updates**: O(1) for most operations
- **History Append**: O(1) amortized with deque
- **History Retrieval**: O(k) where k = requested limit
- **Lock Contention**: Minimal due to fast operations

### Future Scalability Options
1. **Database Backend**: For persistent storage and larger histories
2. **Time-Series Database**: Optimized for metric storage (InfluxDB, Prometheus)
3. **Message Queue**: Async processing of high-frequency requests
4. **Caching Layer**: Redis for frequently accessed data
5. **Sharding**: Multiple PerformanceMetrics instances for different agents

## Security Considerations

### Current Implementation
- **Input Validation**: All user inputs validated
- **Type Checking**: Strict type requirements
- **Duration Capping**: Max 5 seconds to prevent resource abuse
- **Size Limits**: History and log sizes capped

### Recommendations for Production
1. **Authentication**: Add API key or token-based auth
2. **Rate Limiting**: Prevent request flooding
3. **HTTPS**: Encrypt dashboard communication
4. **CORS**: Configure allowed origins
5. **Sanitization**: Already implemented for task names

## Error Handling Strategy

```
API Request
    │
    ▼
Input Validation
    │
    ├─ Type Check ──► Fail ──► Return error response
    ├─ Range Check ──► Fail ──► Return error response
    └─ Pass
    │
    ▼
Execute Operation
    │
    ├─ Success ──► Return success response
    └─ Exception ──► Catch ──► Log ──► Return error response
```

## Testing Architecture

```
test_performance_dashboard.py
│
├─ TestPerformanceMetrics
│   ├─ Unit tests for PerformanceMetrics class
│   ├─ Thread safety tests
│   └─ Edge case tests
│
├─ TestAPIFunctions
│   ├─ Tests for all 6 API endpoints
│   ├─ Parameter validation tests
│   └─ Load testing (100 requests)
│
└─ TestEdgeCases
    ├─ Boundary condition tests
    ├─ Invalid input tests
    └─ Special character tests
```

## Deployment Architecture

```
Production Environment
│
├─ MCP Server Process
│   └─ performance_dashboard_server.py
│       ├─ Listens on MCP protocol
│       └─ Manages PerformanceMetrics instance
│
└─ Web Server (optional)
    └─ Serves dashboard.html
        ├─ Static file serving
        └─ CORS configuration
```

## Monitoring the Monitor

The dashboard itself can be monitored by:
1. Tracking its own API response times
2. Monitoring server process health
3. Checking dashboard auto-refresh functionality
4. Alerting on error log growth
5. Tracking metric calculation accuracy

## Integration Points

### With MCP Framework
- Registered as MCP server with 6 tools
- Follows FastMCP protocol conventions
- Returns structured JSON responses

### With Other Services
- Can monitor any agent tasks
- Extensible to track custom metrics
- API-first design for easy integration

## Performance Optimization

### Current Optimizations
1. **Deque Data Structure**: O(1) append operations
2. **Pre-calculated Rates**: Updated on each request
3. **Minimal Locking**: Lock only during updates/reads
4. **Lazy Evaluation**: Metrics computed only when requested

### Future Optimizations
1. **Batching**: Batch metric updates
2. **Async Processing**: Non-blocking metric recording
3. **Compression**: Compress historical data
4. **Indexing**: Index by timestamp for faster queries
