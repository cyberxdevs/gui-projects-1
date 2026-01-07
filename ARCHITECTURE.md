# Arsitektur Aplikasi

Dokumen ini menjelaskan arsitektur dan desain aplikasi GUI Analisis Postur.

## 📐 Arsitektur Overview

Aplikasi ini menggunakan arsitektur **Model-View-Controller (MVC)** yang dimodifikasi untuk GUI desktop:

```
┌─────────────────────────────────────────────────────┐
│                   Main Application                  │
│              (PostureAnalysisApp)                   │
│                                                     │
│  - Manages navigation between dashboards           │
│  - Stores shared data (user, analysis, results)    │
│  - Coordinates between components                   │
└────────────┬──────────────────────────┬─────────────┘
             │                          │
             ▼                          ▼
    ┌────────────────┐         ┌────────────────┐
    │   GUI Layer    │         │ Analysis Layer │
    │  (Dashboards)  │         │   (Logic)      │
    └────────┬───────┘         └────────┬───────┘
             │                          │
             ▼                          ▼
    ┌─────────────────────────────────────────┐
    │         Utilities & Config              │
    │  (Image Utils, Export, Configuration)   │
    └─────────────────────────────────────────┘
```

## 🏗️ Layer Architecture

### 1. Presentation Layer (GUI)

**Location**: `src/gui/`

**Components**:
- `Dashboard1`: Input form untuk nama dan tinggi
- `Dashboard2`: Upload interface dan konfigurasi
- `Dashboard3`: Visualisasi real-time analisis
- `Dashboard4`: Results display dan export

**Responsibilities**:
- User interface rendering
- User input validation
- Event handling
- Navigation between screens
- Display data dari analysis layer

**Design Pattern**: Each dashboard is a separate Frame component yang dapat di-swap oleh main controller.

### 2. Business Logic Layer (Analysis)

**Location**: `src/analysis/`

**Components**:
- `YOLOAnalyzer`: Wrapper untuk YOLO model inference
- `PostureAnalyzer`: Logic untuk analisis postur dari keypoints

**Responsibilities**:
- Model loading dan inference
- Keypoint detection dan parsing
- Posture classification
- Imbalance calculation
- Score calculation
- Report generation

**Key Algorithms**:

#### Shoulder Imbalance
```python
shoulder_diff = abs(left_shoulder_y - right_shoulder_y)
shoulder_imbalance_mm = shoulder_diff * ratio_mm_per_px
```

#### Hip Imbalance
```python
hip_diff = abs(left_hip_y - right_hip_y)
hip_imbalance_mm = hip_diff * ratio_mm_per_px
```

#### Spine Deviation
```python
shoulder_mid = (left_shoulder_x + right_shoulder_x) / 2
hip_mid = (left_hip_x + right_hip_x) / 2
spine_deviation = abs(shoulder_mid - hip_mid) * ratio_mm_per_px
```

#### Head Shift (Side View)
```python
head_shift = abs(nose_x - shoulder_mid_x) * ratio_mm_per_px
```

#### Head Tilt
```python
angle = atan2(right_eye_y - left_eye_y, right_eye_x - left_eye_x)
head_tilt = abs(degrees(angle))
```

### 3. Utility Layer

**Location**: `src/utils/`

**Components**:
- `image_utils.py`: Image processing functions
- `export_utils.py`: CSV export functions

**Responsibilities**:
- Image loading dan preprocessing
- Image annotation (bounding boxes, keypoints)
- Image resizing untuk display
- CSV generation dan formatting
- Status classification

### 4. Configuration Layer

**Location**: `config/`

**Components**:
- `config.py`: Central configuration file

**Contains**:
- Application settings (window size, colors)
- Path configurations
- YOLO settings (confidence thresholds)
- Posture mapping dictionaries
- Keypoint definitions
- Helper functions

## 🔄 Data Flow

### Analysis Flow

```
1. User Input (Dashboard 1)
   ↓
2. Upload Model & Images (Dashboard 2)
   ↓
3. YOLOAnalyzer.predict()
   - Load model
   - Run inference
   - Extract detections & keypoints
   ↓
4. PostureAnalyzer.analyze()
   - Parse keypoints
   - Calculate imbalances
   - Generate classification
   - Calculate scores
   ↓
5. Visualization (Dashboard 3)
   - Annotate images
   - Display before/after
   - Show analysis info
   ↓
6. Results Display (Dashboard 4)
   - Show tables
   - Generate summary
   - Export CSV
```

### State Management

Main application (PostureAnalysisApp) maintains 3 data stores:

```python
user_data = {
    'name': str,
    'height': float (mm)
}

analysis_data = {
    'model_path': str,
    'image_paths': list[str],
    'confidence': float
}

results_data = list[{
    'image_path': str,
    'yolo_results': dict,
    'posture_results': dict,
    'original_img': ndarray,
    'annotated_img': ndarray,
    'combined_img': ndarray,
    'report_text': str
}]
```

## 🎨 Design Patterns

### 1. Controller Pattern
`PostureAnalysisApp` acts as the main controller:
- Manages dashboard lifecycle
- Handles navigation
- Stores shared state
- Provides data to dashboards

### 2. Observer Pattern
Dashboards observe user actions and trigger appropriate callbacks:
- Button clicks
- File selections
- Form submissions

### 3. Strategy Pattern
Different analysis strategies for different views:
- `back_front_analysis`: Shoulder, Hip, Spine
- `side_analysis`: Head Shift, Head Tilt

### 4. Factory Pattern
Dashboard creation based on dashboard number:
```python
def show_dashboard(dashboard_number):
    if dashboard_number == 1:
        dashboard = Dashboard1(...)
    elif dashboard_number == 2:
        dashboard = Dashboard2(...)
    # ...
```

## 🔌 Extension Points

### Adding New Analysis Type

1. Add to `ANALYSIS_TYPE_MAPPING` in config
2. Implement analysis method in `PostureAnalyzer`:
```python
def _analyze_new_type(self, keypoints, ratio):
    # Implementation
    return imbalance_dict
```
3. Update report generation

### Adding New Dashboard

1. Create new file: `src/gui/dashboard_X.py`
2. Inherit from `tk.Frame`
3. Implement `setup_ui()` method
4. Add to `show_dashboard()` in main.py

### Adding New Export Format

1. Create export function in `export_utils.py`:
```python
def export_to_excel(analysis_results, user_name, output_dir):
    # Implementation
    return filepath
```
2. Add button in Dashboard 4
3. Connect to export function

## 🧪 Testing Strategy

### Unit Testing
- Test each analysis function independently
- Mock YOLO model for testing
- Test image utility functions

### Integration Testing
- Test full analysis flow
- Test data flow between components
- Test export functionality

### UI Testing
- Manual testing of each dashboard
- Test navigation flow
- Test error handling

## 🚀 Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Dashboards created only when needed
2. **Threading**: Analysis runs in separate thread (Dashboard 3)
3. **Image Resizing**: Images resized for display to reduce memory
4. **Batch Processing**: Support for multiple images
5. **Caching**: Results stored in memory for quick access

### Memory Management

- Images stored as numpy arrays (efficient)
- Results stored only during session
- Old dashboard destroyed when switching

## 🔒 Security Considerations

1. **Input Validation**:
   - File type validation for images and models
   - Range validation for numeric inputs

2. **Path Safety**:
   - Use `os.path.join()` for path construction
   - Validate file existence before operations

3. **Error Handling**:
   - Try-catch blocks for file operations
   - User-friendly error messages
   - Logging for debugging

## 📈 Scalability

### Current Limitations
- Single-threaded analysis per session
- In-memory result storage
- Desktop-only deployment

### Potential Improvements
1. **Database Integration**: Store results in database
2. **Cloud Deployment**: Convert to web application
3. **Multi-threading**: Parallel processing for batch analysis
4. **Model Optimization**: Use ONNX or TensorRT for faster inference
5. **Distributed Processing**: Queue system for large batches

## 🌐 Web Integration Architecture

### Option 1: REST API

```
┌──────────────┐      HTTP      ┌──────────────┐
│   Frontend   │ ←────────────→ │   Backend    │
│  (React/Vue) │                │ (Flask/FastAPI)│
└──────────────┘                └───────┬──────┘
                                        │
                                        ▼
                                ┌────────────────┐
                                │ Analysis Logic │
                                │ (Reused Code)  │
                                └────────────────┘
```

### Option 2: Streamlit

```
┌─────────────────────────────────────┐
│        Streamlit Application        │
│  ┌─────────────────────────────┐   │
│  │   UI Components (Widgets)   │   │
│  └──────────┬──────────────────┘   │
│             ▼                       │
│  ┌─────────────────────────────┐   │
│  │    Analysis Logic (Reused)  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## 📝 Code Organization Principles

1. **Separation of Concerns**: GUI, logic, and utilities separated
2. **Single Responsibility**: Each module has one clear purpose
3. **DRY (Don't Repeat Yourself)**: Shared code in utilities
4. **Modularity**: Components can be tested independently
5. **Configurability**: Settings centralized in config

## 🔧 Development Workflow

```
1. Plan Feature
   ↓
2. Update Architecture (if needed)
   ↓
3. Implement in appropriate layer
   ↓
4. Test independently
   ↓
5. Integration test
   ↓
6. Update documentation
   ↓
7. Commit with clear message
```

---

**This architecture ensures maintainability, scalability, and clean separation of concerns.**
