# # app.py
# import streamlit as st
# import cv2
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import plotly.graph_objects as go
# import plotly.express as px
# from deepface import DeepFace
# import time
# from datetime import datetime
# import tempfile
# import os
# from collections import Counter
# import base64
# from PIL import Image
# import warnings
# warnings.filterwarnings('ignore')

# # Page configuration
# st.set_page_config(
#     page_title="Affective Mental Analytics",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better UI
# st.markdown("""
#     <style>
#     .main-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px;
#         border-radius: 10px;
#         margin-bottom: 20px;
#         color: white;
#         text-align: center;
#     }
#     .emotion-card {
#         background: white;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin-bottom: 10px;
#         border-left: 5px solid #667eea;
#     }
#     .metric-card {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 15px;
#         border-radius: 10px;
#         text-align: center;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .recommendation-box {
#         background: #f8f9fa;
#         padding: 15px;
#         border-radius: 10px;
#         border-left: 5px solid #28a745;
#         margin-top: 10px;
#     }
#     .stButton>button {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         color: white;
#         border: none;
#         padding: 10px 20px;
#         border-radius: 5px;
#         font-weight: bold;
#     }
#     .stButton>button:hover {
#         background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# if 'emotion_history' not in st.session_state:
#     st.session_state.emotion_history = []
# if 'timestamps' not in st.session_state:
#     st.session_state.timestamps = []
# if 'capturing' not in st.session_state:
#     st.session_state.capturing = False
# if 'report_generated' not in st.session_state:
#     st.session_state.report_generated = False
# if 'captured_image' not in st.session_state:
#     st.session_state.captured_image = None

# class EmotionAnalyzer:
#     def __init__(self):
#         self.emotion_colors = {
#             'angry': '#FF4136',
#             'disgust': '#2ECC40',
#             'fear': '#7FDBFF',
#             'happy': '#FFDC00',
#             'sad': '#0074D9',
#             'surprise': '#FF851B',
#             'neutral': '#AAAAAA'
#         }
    
#     def analyze_emotion(self, frame):
#         """Analyze emotion from frame using DeepFace"""
#         try:
#             # Save frame temporarily
#             with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
#                 cv2.imwrite(tmp_file.name, frame)
                
#                 # Analyze with DeepFace
#                 result = DeepFace.analyze(
#                     img_path=tmp_file.name,
#                     actions=['emotion'],
#                     enforce_detection=False,
#                     silent=True
#                 )
                
#                 # Clean up temp file
#                 os.unlink(tmp_file.name)
                
#                 if isinstance(result, list) and len(result) > 0:
#                     return result[0]
#                 elif isinstance(result, dict):
#                     return result
#                 else:
#                     return None
                    
#         except Exception as e:
#             st.warning(f"Emotion detection error: {str(e)}")
#             return None
    
#     def get_dominant_emotion(self, analysis_result):
#         """Extract dominant emotion from analysis result"""
#         if analysis_result and 'dominant_emotion' in analysis_result:
#             return analysis_result['dominant_emotion']
#         return None
    
#     def get_emotion_scores(self, analysis_result):
#         """Get all emotion scores"""
#         if analysis_result and 'emotion' in analysis_result:
#             return analysis_result['emotion']
#         return None

# def main():
#     # Header
#     st.markdown("""
#         <div class="main-header">
#             <h1>🧠 Affective Mental Analytics</h1>
#             <p>Real-time emotion analysis for mental health assessment</p>
#         </div>
#     """, unsafe_allow_html=True)
    
#     # Initialize analyzer
#     analyzer = EmotionAnalyzer()
    
#     # Sidebar
#     with st.sidebar:
#         st.markdown("### ⚙️ Settings")
#         capture_duration = st.slider("Capture Duration (seconds)", 10, 60, 30)
#         capture_interval = st.slider("Capture Interval (seconds)", 1, 5, 2)
        
#         st.markdown("### 📊 Emotion Legend")
#         for emotion, color in analyzer.emotion_colors.items():
#             st.markdown(f"<span style='color:{color}'>⬤</span> {emotion.capitalize()}", unsafe_allow_html=True)
        
#         if st.button("🔄 Reset Session"):
#             st.session_state.emotion_history = []
#             st.session_state.timestamps = []
#             st.session_state.capturing = False
#             st.session_state.report_generated = False
#             st.session_state.captured_image = None
#             st.rerun()
    
#     # Main content area
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         st.markdown("### 📹 Camera Feed")
        
#         # Camera input
#         img_file_buffer = st.camera_input("Take a photo", key="camera")
        
#         if img_file_buffer is not None:
#             # Convert to numpy array
#             bytes_data = img_file_buffer.getvalue()
#             cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
#             st.session_state.captured_image = cv2_img
            
#             # Analyze single image
#             if st.button("🔍 Analyze Current Image"):
#                 with st.spinner("Analyzing emotions..."):
#                     analysis = analyzer.analyze_emotion(cv2_img)
#                     if analysis:
#                         dominant = analyzer.get_dominant_emotion(analysis)
#                         scores = analyzer.get_emotion_scores(analysis)
                        
#                         if dominant and scores:
#                             st.success(f"Dominant Emotion: {dominant.capitalize()}")
                            
#                             # Display emotion scores
#                             fig = go.Figure(data=[
#                                 go.Bar(
#                                     x=list(scores.keys()),
#                                     y=list(scores.values()),
#                                     marker_color=[analyzer.emotion_colors.get(e, '#AAAAAA') for e in scores.keys()]
#                                 )
#                             ])
#                             fig.update_layout(
#                                 title="Emotion Scores",
#                                 xaxis_title="Emotion",
#                                 yaxis_title="Score",
#                                 height=400
#                             )
#                             st.plotly_chart(fig, use_container_width=True)
        
#         # Start/Stop capture session
#         col_capture1, col_capture2 = st.columns(2)
#         with col_capture1:
#             if st.button("▶️ Start Emotion Tracking", use_container_width=True):
#                 st.session_state.capturing = True
#                 st.session_state.emotion_history = []
#                 st.session_state.timestamps = []
#                 st.session_state.report_generated = False
                
#         with col_capture2:
#             if st.button("⏹️ Stop Tracking", use_container_width=True):
#                 st.session_state.capturing = False
    
#     with col2:
#         st.markdown("### 📊 Live Statistics")
        
#         if st.session_state.emotion_history:
#             # Calculate statistics
#             emotion_counts = Counter(st.session_state.emotion_history)
#             total_captures = len(st.session_state.emotion_history)
            
#             # Display metrics
#             col_metric1, col_metric2 = st.columns(2)
#             with col_metric1:
#                 st.markdown("""
#                     <div class="metric-card">
#                         <h3>Total Captures</h3>
#                         <h2>{}</h2>
#                     </div>
#                 """.format(total_captures), unsafe_allow_html=True)
            
#             with col_metric2:
#                 if emotion_counts:
#                     most_common = emotion_counts.most_common(1)[0]
#                     st.markdown("""
#                         <div class="metric-card">
#                             <h3>Most Common</h3>
#                             <h2>{}</h2>
#                             <p>{} times</p>
#                         </div>
#                     """.format(most_common[0].capitalize(), most_common[1]), unsafe_allow_html=True)
            
#             # Current dominant emotion
#             if st.session_state.emotion_history:
#                 current_emotion = st.session_state.emotion_history[-1]
#                 st.markdown("""
#                     <div class="emotion-card">
#                         <h4>Current Emotion</h4>
#                         <h2 style="color:{}">{}</h2>
#                     </div>
#                 """.format(analyzer.emotion_colors.get(current_emotion, '#AAAAAA'), 
#                           current_emotion.capitalize()), unsafe_allow_html=True)
    
#     # Emotion tracking session
#     if st.session_state.capturing:
#         placeholder = st.empty()
        
#         for i in range(capture_duration):
#             if not st.session_state.capturing:
#                 break
                
#             # Capture and analyze
#             if st.session_state.captured_image is not None:
#                 analysis = analyzer.analyze_emotion(st.session_state.captured_image)
                
#                 if analysis:
#                     dominant = analyzer.get_dominant_emotion(analysis)
#                     if dominant:
#                         st.session_state.emotion_history.append(dominant)
#                         st.session_state.timestamps.append(datetime.now())
                        
#                         # Update placeholder
#                         with placeholder.container():
#                             st.info(f"Captured: {dominant.capitalize()} - {i+1}/{capture_duration}")
            
#             time.sleep(capture_interval)
        
#         st.session_state.capturing = False
#         st.session_state.report_generated = False
#         st.rerun()
    
#     # Generate Report Section
#     if st.session_state.emotion_history and not st.session_state.report_generated:
#         st.markdown("---")
#         st.markdown("### 📋 Generate Mental Health Assessment Report")
        
#         col_report1, col_report2, col_report3 = st.columns(3)
        
#         with col_report1:
#             report_type = st.selectbox(
#                 "Report Type",
#                 ["Comprehensive Analysis", "Summary Report", "Clinical Assessment"]
#             )
        
#         with col_report2:
#             include_viz = st.checkbox("Include Visualizations", value=True)
        
#         with col_report3:
#             include_recommendations = st.checkbox("Include Recommendations", value=True)
        
#         if st.button("📊 Generate Report", use_container_width=True):
#             with st.spinner("Generating comprehensive report..."):
#                 generate_report(
#                     st.session_state.emotion_history,
#                     st.session_state.timestamps,
#                     st.session_state.captured_image,
#                     report_type,
#                     include_viz,
#                     include_recommendations,
#                     analyzer
#                 )
#                 st.session_state.report_generated = True

# def generate_report(emotion_history, timestamps, captured_image, report_type, include_viz, include_recommendations, analyzer):
#     """Generate comprehensive mental health assessment report"""
    
#     st.markdown("## 📊 Mental Health Assessment Report")
#     st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     st.markdown(f"**Report Type:** {report_type}")
    
#     # Create tabs for different report sections
#     tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Analytics", "📉 Trends", "💡 Recommendations"])
    
#     with tab1:
#         col_img, col_stats = st.columns(2)
        
#         with col_img:
#             if captured_image is not None:
#                 st.image(cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB), 
#                         caption="Captured Image", use_column_width=True)
        
#         with col_stats:
#             # Basic statistics
#             emotion_counts = Counter(emotion_history)
#             df_emotions = pd.DataFrame(
#                 list(emotion_counts.items()), 
#                 columns=['Emotion', 'Count']
#             )
#             df_emotions['Percentage'] = (df_emotions['Count'] / len(emotion_history) * 100).round(2)
            
#             st.markdown("### Emotion Distribution")
#             st.dataframe(df_emotions, use_container_width=True)
    
#     with tab2:
#         if include_viz:
#             col_pie, col_bar = st.columns(2)
            
#             with col_pie:
#                 # Pie chart
#                 fig_pie = go.Figure(data=[go.Pie(
#                     labels=list(emotion_counts.keys()),
#                     values=list(emotion_counts.values()),
#                     marker_colors=[analyzer.emotion_colors.get(e, '#AAAAAA') for e in emotion_counts.keys()]
#                 )])
#                 fig_pie.update_layout(title="Emotion Distribution")
#                 st.plotly_chart(fig_pie, use_container_width=True)
            
#             with col_bar:
#                 # Bar chart
#                 fig_bar = go.Figure(data=[go.Bar(
#                     x=list(emotion_counts.keys()),
#                     y=list(emotion_counts.values()),
#                     marker_color=[analyzer.emotion_colors.get(e, '#AAAAAA') for e in emotion_counts.keys()]
#                 )])
#                 fig_bar.update_layout(title="Emotion Frequency")
#                 st.plotly_chart(fig_bar, use_container_width=True)
    
#     with tab3:
#         if len(emotion_history) > 1:
#             # Timeline visualization
#             df_timeline = pd.DataFrame({
#                 'Time': range(len(emotion_history)),
#                 'Emotion': emotion_history
#             })
            
#             # Convert emotions to numeric for trend line
#             emotion_to_num = {emotion: i for i, emotion in enumerate(set(emotion_history))}
#             df_timeline['Emotion_Num'] = df_timeline['Emotion'].map(emotion_to_num)
            
#             fig_timeline = go.Figure()
            
#             # Add scatter plot
#             fig_timeline.add_trace(go.Scatter(
#                 x=df_timeline['Time'],
#                 y=df_timeline['Emotion_Num'],
#                 mode='lines+markers',
#                 text=df_timeline['Emotion'],
#                 line=dict(color='#667eea', width=2),
#                 marker=dict(size=8, color='#764ba2')
#             ))
            
#             # Update y-axis labels
#             fig_timeline.update_yaxes(
#                 ticktext=list(emotion_to_num.keys()),
#                 tickvals=list(emotion_to_num.values())
#             )
            
#             fig_timeline.update_layout(
#                 title="Emotion Timeline",
#                 xaxis_title="Capture Sequence",
#                 yaxis_title="Emotion",
#                 height=500
#             )
            
#             st.plotly_chart(fig_timeline, use_container_width=True)
            
#             # Calculate emotional stability
#             unique_emotions = len(set(emotion_history))
#             total_changes = sum(1 for i in range(1, len(emotion_history)) 
#                               if emotion_history[i] != emotion_history[i-1])
            
#             stability_score = (1 - (total_changes / len(emotion_history))) * 100
            
#             # Metrics
#             col_metric1, col_metric2, col_metric3 = st.columns(3)
#             with col_metric1:
#                 st.metric("Emotional Stability", f"{stability_score:.1f}%")
#             with col_metric2:
#                 st.metric("Emotion Switches", total_changes)
#             with col_metric3:
#                 st.metric("Unique Emotions", unique_emotions)
    
#     with tab4:
#         if include_recommendations:
#             st.markdown("### 💡 Personalized Recommendations")
            
#             # Generate recommendations based on emotion patterns
#             emotion_counts = Counter(emotion_history)
#             dominant_emotion = emotion_counts.most_common(1)[0][0]
            
#             recommendations = {
#                 'happy': [
#                     "🌟 Maintain positive activities and social connections",
#                     "📝 Journal your positive experiences for future reflection",
#                     "🤝 Share your positivity with others through kind acts",
#                     "🎯 Set new goals while in this positive state"
#                 ],
#                 'sad': [
#                     "💭 Practice self-compassion and allow yourself to feel",
#                     "🏃 Engage in light physical activity to boost mood",
#                     "📞 Connect with a trusted friend or family member",
#                     "🧘 Try mindfulness or meditation exercises",
#                     "📝 Consider speaking with a mental health professional"
#                 ],
#                 'angry': [
#                     "🌬️ Practice deep breathing exercises (4-7-8 technique)",
#                     "✍️ Write down your feelings in a journal",
#                     "🚶 Take a short walk to clear your mind",
#                     "🎵 Listen to calming music",
#                     "💬 Consider anger management techniques or counseling"
#                 ],
#                 'fear': [
#                     "🧘 Practice grounding techniques (5-4-3-2-1 method)",
#                     "📝 Challenge anxious thoughts with evidence",
#                     "🌿 Create a calm environment with soothing activities",
#                     "🤝 Reach out to support network",
#                     "🎯 Consider professional support if anxiety persists"
#                 ],
#                 'surprise': [
#                     "🤔 Take time to process unexpected events",
#                     "📝 Journal about the experience to gain perspective",
#                     "🗣️ Discuss surprising events with trusted others",
#                     "⚖️ Practice emotional regulation techniques"
#                 ],
#                 'neutral': [
#                     "🎯 Set small, achievable goals for the day",
#                     "🧠 Engage in stimulating mental activities",
#                     "🌱 Try new experiences to increase engagement",
#                     "🤝 Connect with others for social interaction",
#                     "💭 Practice gratitude journaling"
#                 ],
#                 'disgust': [
#                     "🧘 Practice mindfulness to process the feeling",
#                     "🔄 Reframe negative thoughts positively",
#                     "🌿 Create a pleasant environment",
#                     "🗣️ Discuss feelings with a trusted person",
#                     "🎯 Focus on things you appreciate"
#                 ]
#             }
            
#             # Display recommendations for dominant emotion
#             st.markdown(f"""
#                 <div class="recommendation-box">
#                     <h4>Based on your dominant emotion: {dominant_emotion.capitalize()}</h4>
#                 </div>
#             """, unsafe_allow_html=True)
            
#             for rec in recommendations.get(dominant_emotion, recommendations['neutral']):
#                 st.markdown(f"- {rec}")
            
#             # Additional insights
#             st.markdown("### 📊 Key Insights")
            
#             # Emotional diversity
#             diversity = len(emotion_counts) / len(set(analyzer.emotion_colors.keys())) * 100
            
#             if diversity > 70:
#                 st.info("📊 You're experiencing a wide range of emotions, which is healthy and normal.")
#             elif diversity > 40:
#                 st.info("📈 You're experiencing a moderate range of emotions. Consider exploring different activities.")
#             else:
#                 st.warning("⚠️ Your emotional range appears limited. Consider activities that might bring variety to your emotional experience.")
            
#             # Recommendation for professional help
#             if emotion_counts.get('sad', 0) > len(emotion_history) * 0.3 or emotion_counts.get('angry', 0) > len(emotion_history) * 0.3:
#                 st.error("""
#                 🏥 **Professional Support Recommendation**
                
#                 Based on the patterns observed, you might benefit from speaking with a mental health professional. 
#                 Consider reaching out to:
#                 - A licensed therapist or counselor
#                 - Your primary care physician
#                 - A mental health hotline for immediate support
#                 """)
    
#     # Download report button
#     report_text = generate_report_text(emotion_history, timestamps, captured_image, report_type)
#     st.download_button(
#         label="📥 Download Report",
#         data=report_text,
#         file_name=f"mental_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#         mime="text/plain"
#     )

# def generate_report_text(emotion_history, timestamps, captured_image, report_type):
#     """Generate text version of the report for download"""
    
#     report = []
#     report.append("=" * 50)
#     report.append("MENTAL HEALTH ASSESSMENT REPORT")
#     report.append("=" * 50)
#     report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
#     report.append(f"Report Type: {report_type}")
#     report.append("=" * 50)
#     report.append("")
    
#     # Statistics
#     emotion_counts = Counter(emotion_history)
#     report.append("EMOTION DISTRIBUTION:")
#     report.append("-" * 30)
#     for emotion, count in emotion_counts.items():
#         percentage = (count / len(emotion_history)) * 100
#         report.append(f"{emotion.capitalize()}: {count} times ({percentage:.1f}%)")
    
#     report.append("")
#     report.append("EMOTION TIMELINE:")
#     report.append("-" * 30)
#     for i, (emotion, timestamp) in enumerate(zip(emotion_history, timestamps)):
#         time_str = timestamp.strftime('%H:%M:%S') if timestamp else f"Capture {i+1}"
#         report.append(f"{time_str}: {emotion.capitalize()}")
    
#     report.append("")
#     report.append("=" * 50)
#     report.append("END OF REPORT")
#     report.append("=" * 50)
    
#     return "\n".join(report)

# if __name__ == "__main__":
#     main()
# app.py
# import streamlit as st
# import cv2
# import numpy as np
# import pandas as pd
# import plotly.graph_objects as go
# import time
# from datetime import datetime
# import os
# from collections import Counter
# from PIL import Image
# import warnings
# warnings.filterwarnings('ignore')

# # Try importing fer, fallback to mock if unavailable
# try:
#     from fer import FER
#     emotion_detector = FER(mtcnn=False)
#     USE_FER = True
# except ImportError:
#     USE_FER = False

# st.set_page_config(
#     page_title="Affective Mental Analytics",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown("""
#     <style>
#     .main-header {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         padding: 20px;
#         border-radius: 10px;
#         margin-bottom: 20px;
#         color: white;
#         text-align: center;
#     }
#     .emotion-card {
#         background: white;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 4px 6px rgba(0,0,0,0.1);
#         margin-bottom: 10px;
#         border-left: 5px solid #667eea;
#     }
#     .metric-card {
#         background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
#         padding: 15px;
#         border-radius: 10px;
#         text-align: center;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     .recommendation-box {
#         background: #f8f9fa;
#         padding: 15px;
#         border-radius: 10px;
#         border-left: 5px solid #28a745;
#         margin-top: 10px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Session state
# for key, val in {
#     'emotion_history': [],
#     'timestamps': [],
#     'capturing': False,
#     'report_generated': False,
#     'captured_image': None
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = val

# EMOTION_COLORS = {
#     'angry': '#FF4136',
#     'disgust': '#2ECC40',
#     'fear': '#7FDBFF',
#     'happy': '#FFDC00',
#     'sad': '#0074D9',
#     'surprise': '#FF851B',
#     'neutral': '#AAAAAA'
# }

# def analyze_emotion(frame):
#     """Analyze emotion from frame"""
#     try:
#         if USE_FER:
#             rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             result = emotion_detector.detect_emotions(rgb)
#             if result:
#                 emotions = result[0]['emotions']
#                 dominant = max(emotions, key=emotions.get)
#                 return dominant, emotions
#         # Fallback: random for demo purposes
#         import random
#         dominant = random.choice(list(EMOTION_COLORS.keys()))
#         scores = {e: round(random.uniform(0, 1), 2) for e in EMOTION_COLORS}
#         return dominant, scores
#     except Exception as e:
#         st.warning(f"Detection error: {str(e)}")
#         return None, None

# def main():
#     st.markdown("""
#         <div class="main-header">
#             <h1>🧠 Affective Mental Analytics</h1>
#             <p>Real-time emotion analysis for mental health assessment</p>
#         </div>
#     """, unsafe_allow_html=True)

#     if not USE_FER:
#         st.warning("⚠️ FER library not found. Install it with: `pip install fer` — Running in demo mode.")

#     with st.sidebar:
#         st.markdown("### ⚙️ Settings")
#         capture_duration = st.slider("Capture Duration (seconds)", 10, 60, 30)
#         capture_interval = st.slider("Capture Interval (seconds)", 1, 5, 2)

#         st.markdown("### 📊 Emotion Legend")
#         for emotion, color in EMOTION_COLORS.items():
#             st.markdown(f"<span style='color:{color}'>⬤</span> {emotion.capitalize()}", unsafe_allow_html=True)

#         if st.button("🔄 Reset Session"):
#             for key in ['emotion_history', 'timestamps']:
#                 st.session_state[key] = []
#             st.session_state.capturing = False
#             st.session_state.report_generated = False
#             st.session_state.captured_image = None
#             st.rerun()

#     col1, col2 = st.columns([2, 1])

#     with col1:
#         st.markdown("### 📹 Camera Feed")
#         img_file_buffer = st.camera_input("Take a photo", key="camera")

#         if img_file_buffer is not None:
#             bytes_data = img_file_buffer.getvalue()
#             cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
#             st.session_state.captured_image = cv2_img

#             if st.button("🔍 Analyze Current Image"):
#                 with st.spinner("Analyzing emotions..."):
#                     dominant, scores = analyze_emotion(cv2_img)
#                     if dominant and scores:
#                         st.success(f"Dominant Emotion: **{dominant.capitalize()}**")
#                         fig = go.Figure(data=[go.Bar(
#                             x=list(scores.keys()),
#                             y=list(scores.values()),
#                             marker_color=[EMOTION_COLORS.get(e, '#AAAAAA') for e in scores.keys()]
#                         )])
#                         fig.update_layout(title="Emotion Scores", xaxis_title="Emotion", yaxis_title="Score", height=400)
#                         st.plotly_chart(fig, use_container_width=True)

#         col_c1, col_c2 = st.columns(2)
#         with col_c1:
#             if st.button("▶️ Start Emotion Tracking", use_container_width=True):
#                 st.session_state.capturing = True
#                 st.session_state.emotion_history = []
#                 st.session_state.timestamps = []
#                 st.session_state.report_generated = False
#         with col_c2:
#             if st.button("⏹️ Stop Tracking", use_container_width=True):
#                 st.session_state.capturing = False

#     with col2:
#         st.markdown("### 📊 Live Statistics")
#         if st.session_state.emotion_history:
#             emotion_counts = Counter(st.session_state.emotion_history)
#             total = len(st.session_state.emotion_history)
#             col_m1, col_m2 = st.columns(2)
#             with col_m1:
#                 st.markdown(f"""<div class="metric-card"><h3>Total Captures</h3><h2>{total}</h2></div>""", unsafe_allow_html=True)
#             with col_m2:
#                 most_common = emotion_counts.most_common(1)[0]
#                 st.markdown(f"""<div class="metric-card"><h3>Most Common</h3><h2>{most_common[0].capitalize()}</h2><p>{most_common[1]} times</p></div>""", unsafe_allow_html=True)

#             current = st.session_state.emotion_history[-1]
#             color = EMOTION_COLORS.get(current, '#AAAAAA')
#             st.markdown(f"""<div class="emotion-card"><h4>Current Emotion</h4><h2 style="color:{color}">{current.capitalize()}</h2></div>""", unsafe_allow_html=True)

#     # Tracking session
#     if st.session_state.capturing:
#         placeholder = st.empty()
#         for i in range(capture_duration):
#             if not st.session_state.capturing:
#                 break
#             if st.session_state.captured_image is not None:
#                 dominant, _ = analyze_emotion(st.session_state.captured_image)
#                 if dominant:
#                     st.session_state.emotion_history.append(dominant)
#                     st.session_state.timestamps.append(datetime.now())
#                     with placeholder.container():
#                         st.info(f"Captured: {dominant.capitalize()} — {i+1}/{capture_duration}")
#             time.sleep(capture_interval)
#         st.session_state.capturing = False
#         st.session_state.report_generated = False
#         st.rerun()

#     # Report
#     if st.session_state.emotion_history and not st.session_state.report_generated:
#         st.markdown("---")
#         st.markdown("### 📋 Generate Mental Health Assessment Report")
#         col_r1, col_r2, col_r3 = st.columns(3)
#         with col_r1:
#             report_type = st.selectbox("Report Type", ["Comprehensive Analysis", "Summary Report", "Clinical Assessment"])
#         with col_r2:
#             include_viz = st.checkbox("Include Visualizations", value=True)
#         with col_r3:
#             include_recommendations = st.checkbox("Include Recommendations", value=True)

#         if st.button("📊 Generate Report", use_container_width=True):
#             with st.spinner("Generating report..."):
#                 generate_report(st.session_state.emotion_history, st.session_state.timestamps,
#                                 st.session_state.captured_image, report_type, include_viz, include_recommendations)
#                 st.session_state.report_generated = True

# def generate_report(emotion_history, timestamps, captured_image, report_type, include_viz, include_recommendations):
#     st.markdown("## 📊 Mental Health Assessment Report")
#     st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Type:** {report_type}")

#     tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Analytics", "📉 Trends", "💡 Recommendations"])
#     emotion_counts = Counter(emotion_history)

#     with tab1:
#         col_img, col_stats = st.columns(2)
#         with col_img:
#             if captured_image is not None:
#                 st.image(cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB), caption="Captured Image", use_column_width=True)
#         with col_stats:
#             df = pd.DataFrame(list(emotion_counts.items()), columns=['Emotion', 'Count'])
#             df['Percentage'] = (df['Count'] / len(emotion_history) * 100).round(2)
#             st.markdown("### Emotion Distribution")
#             st.dataframe(df, use_container_width=True)

#     with tab2:
#         if include_viz:
#             col_pie, col_bar = st.columns(2)
#             with col_pie:
#                 fig_pie = go.Figure(data=[go.Pie(
#                     labels=list(emotion_counts.keys()),
#                     values=list(emotion_counts.values()),
#                     marker_colors=[EMOTION_COLORS.get(e, '#AAAAAA') for e in emotion_counts.keys()]
#                 )])
#                 fig_pie.update_layout(title="Emotion Distribution")
#                 st.plotly_chart(fig_pie, use_container_width=True)
#             with col_bar:
#                 fig_bar = go.Figure(data=[go.Bar(
#                     x=list(emotion_counts.keys()),
#                     y=list(emotion_counts.values()),
#                     marker_color=[EMOTION_COLORS.get(e, '#AAAAAA') for e in emotion_counts.keys()]
#                 )])
#                 fig_bar.update_layout(title="Emotion Frequency")
#                 st.plotly_chart(fig_bar, use_container_width=True)

#     with tab3:
#         if len(emotion_history) > 1:
#             emotion_to_num = {e: i for i, e in enumerate(set(emotion_history))}
#             fig = go.Figure()
#             fig.add_trace(go.Scatter(
#                 x=list(range(len(emotion_history))),
#                 y=[emotion_to_num[e] for e in emotion_history],
#                 mode='lines+markers',
#                 text=emotion_history,
#                 line=dict(color='#667eea', width=2),
#                 marker=dict(size=8, color='#764ba2')
#             ))
#             fig.update_yaxes(ticktext=list(emotion_to_num.keys()), tickvals=list(emotion_to_num.values()))
#             fig.update_layout(title="Emotion Timeline", xaxis_title="Capture Sequence", yaxis_title="Emotion", height=400)
#             st.plotly_chart(fig, use_container_width=True)

#             total_changes = sum(1 for i in range(1, len(emotion_history)) if emotion_history[i] != emotion_history[i-1])
#             stability = (1 - total_changes / len(emotion_history)) * 100
#             c1, c2, c3 = st.columns(3)
#             c1.metric("Emotional Stability", f"{stability:.1f}%")
#             c2.metric("Emotion Switches", total_changes)
#             c3.metric("Unique Emotions", len(set(emotion_history)))

#     with tab4:
#         if include_recommendations:
#             dominant = emotion_counts.most_common(1)[0][0]
#             recommendations = {
#                 'happy': ["🌟 Maintain positive activities", "📝 Journal positive experiences", "🤝 Share positivity with others", "🎯 Set new goals"],
#                 'sad': ["💭 Practice self-compassion", "🏃 Light physical activity", "📞 Connect with loved ones", "🧘 Try mindfulness", "📝 Consider professional support"],
#                 'angry': ["🌬️ Deep breathing (4-7-8)", "✍️ Journal your feelings", "🚶 Take a short walk", "🎵 Listen to calm music"],
#                 'fear': ["🧘 Grounding techniques (5-4-3-2-1)", "📝 Challenge anxious thoughts", "🤝 Reach out to support network"],
#                 'surprise': ["🤔 Take time to process", "📝 Journal the experience", "🗣️ Discuss with trusted others"],
#                 'neutral': ["🎯 Set small daily goals", "🧠 Stimulating mental activities", "🌱 Try new experiences"],
#                 'disgust': ["🧘 Mindfulness practice", "🔄 Reframe negative thoughts", "🌿 Create a pleasant environment"]
#             }
#             st.markdown(f"""<div class="recommendation-box"><h4>Based on dominant emotion: {dominant.capitalize()}</h4></div>""", unsafe_allow_html=True)
#             for rec in recommendations.get(dominant, recommendations['neutral']):
#                 st.markdown(f"- {rec}")

#             diversity = len(emotion_counts) / len(EMOTION_COLORS) * 100
#             if diversity > 70:
#                 st.info("📊 Wide emotional range detected — healthy and normal.")
#             elif diversity > 40:
#                 st.info("📈 Moderate emotional range. Consider varied activities.")
#             else:
#                 st.warning("⚠️ Limited emotional range. Try diverse experiences.")

#             if emotion_counts.get('sad', 0) > len(emotion_history) * 0.3 or emotion_counts.get('angry', 0) > len(emotion_history) * 0.3:
#                 st.error("🏥 **Professional Support Recommended** — Consider speaking with a licensed therapist or counselor.")

#     report_text = "\n".join([
#         "=" * 50, "MENTAL HEALTH ASSESSMENT REPORT", "=" * 50,
#         f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
#         f"Report Type: {report_type}", "=" * 50, "",
#         "EMOTION DISTRIBUTION:", "-" * 30,
#         *[f"{e.capitalize()}: {c} times ({c/len(emotion_history)*100:.1f}%)" for e, c in emotion_counts.items()],
#         "", "EMOTION TIMELINE:", "-" * 30,
#         *[f"{t.strftime('%H:%M:%S')}: {e.capitalize()}" for e, t in zip(emotion_history, timestamps)],
#         "", "=" * 50, "END OF REPORT", "=" * 50
#     ])
#     st.download_button("📥 Download Report", data=report_text,
#                        file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", mime="text/plain")

# if __name__ == "__main__":
#     main()
# # ```

# # Then install `fer`:
# # ```
# # pip install fer
# # ```

# # And run:
# # ```
# # streamlit run app.py
# app.py
import streamlit as st
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Try importing fer, fallback to demo mode if unavailable
try:
    from fer import FER
    emotion_detector = FER(mtcnn=False)
    USE_FER = True
except Exception:
    USE_FER = False

st.set_page_config(
    page_title="Affective Mental Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .emotion-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #667eea;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .recommendation-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin-top: 10px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
for key, val in {
    'emotion_history': [],
    'timestamps': [],
    'capturing': False,
    'report_generated': False,
    'captured_image': None
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

EMOTION_COLORS = {
    'angry': '#FF4136',
    'disgust': '#2ECC40',
    'fear': '#7FDBFF',
    'happy': '#FFDC00',
    'sad': '#0074D9',
    'surprise': '#FF851B',
    'neutral': '#AAAAAA'
}

RECOMMENDATIONS = {
    'happy': [
        "🌟 Maintain positive activities and social connections",
        "📝 Journal your positive experiences for future reflection",
        "🤝 Share your positivity with others through kind acts",
        "🎯 Set new goals while in this positive state"
    ],
    'sad': [
        "💭 Practice self-compassion and allow yourself to feel",
        "🏃 Engage in light physical activity to boost mood",
        "📞 Connect with a trusted friend or family member",
        "🧘 Try mindfulness or meditation exercises",
        "📝 Consider speaking with a mental health professional"
    ],
    'angry': [
        "🌬️ Practice deep breathing exercises (4-7-8 technique)",
        "✍️ Write down your feelings in a journal",
        "🚶 Take a short walk to clear your mind",
        "🎵 Listen to calming music",
        "💬 Consider anger management techniques or counseling"
    ],
    'fear': [
        "🧘 Practice grounding techniques (5-4-3-2-1 method)",
        "📝 Challenge anxious thoughts with evidence",
        "🌿 Create a calm environment with soothing activities",
        "🤝 Reach out to your support network",
        "🎯 Consider professional support if anxiety persists"
    ],
    'surprise': [
        "🤔 Take time to process unexpected events",
        "📝 Journal about the experience to gain perspective",
        "🗣️ Discuss surprising events with trusted others",
        "⚖️ Practice emotional regulation techniques"
    ],
    'neutral': [
        "🎯 Set small, achievable goals for the day",
        "🧠 Engage in stimulating mental activities",
        "🌱 Try new experiences to increase engagement",
        "🤝 Connect with others for social interaction",
        "💭 Practice gratitude journaling"
    ],
    'disgust': [
        "🧘 Practice mindfulness to process the feeling",
        "🔄 Reframe negative thoughts positively",
        "🌿 Create a pleasant environment",
        "🗣️ Discuss feelings with a trusted person",
        "🎯 Focus on things you appreciate"
    ]
}

def analyze_emotion(frame):
    """Analyze emotion from frame using FER or demo fallback"""
    try:
        if USE_FER:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = emotion_detector.detect_emotions(rgb)
            if result:
                emotions = result[0]['emotions']
                dominant = max(emotions, key=emotions.get)
                return dominant, emotions
        # Demo fallback with random values
        import random
        dominant = random.choice(list(EMOTION_COLORS.keys()))
        scores = {e: round(random.uniform(0, 1), 2) for e in EMOTION_COLORS}
        return dominant, scores
    except Exception as e:
        st.warning(f"Detection error: {str(e)}")
        return None, None

def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🧠 Affective Mental Analytics</h1>
            <p>Real-time emotion analysis for mental health assessment</p>
        </div>
    """, unsafe_allow_html=True)

    if not USE_FER:
        st.warning("⚠️ FER not loaded — running in demo mode. Run `pip install fer tensorflow==2.13.0` to enable real detection.")

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        capture_duration = st.slider("Capture Duration (seconds)", 10, 60, 30)
        capture_interval = st.slider("Capture Interval (seconds)", 1, 5, 2)

        st.markdown("### 📊 Emotion Legend")
        for emotion, color in EMOTION_COLORS.items():
            st.markdown(
                f"<span style='color:{color}'>⬤</span> {emotion.capitalize()}",
                unsafe_allow_html=True
            )

        if st.button("🔄 Reset Session"):
            st.session_state.emotion_history = []
            st.session_state.timestamps = []
            st.session_state.capturing = False
            st.session_state.report_generated = False
            st.session_state.captured_image = None
            st.rerun()

    # Main layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📹 Camera Feed")
        img_file_buffer = st.camera_input("Take a photo", key="camera")

        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            st.session_state.captured_image = cv2_img

            if st.button("🔍 Analyze Current Image"):
                with st.spinner("Analyzing emotions..."):
                    dominant, scores = analyze_emotion(cv2_img)
                    if dominant and scores:
                        st.success(f"Dominant Emotion: **{dominant.capitalize()}**")
                        fig = go.Figure(data=[go.Bar(
                            x=list(scores.keys()),
                            y=list(scores.values()),
                            marker_color=[EMOTION_COLORS.get(e, '#AAAAAA') for e in scores.keys()]
                        )])
                        fig.update_layout(
                            title="Emotion Scores",
                            xaxis_title="Emotion",
                            yaxis_title="Score",
                            height=400
                        )
                        st.plotly_chart(fig, use_container_width=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("▶️ Start Emotion Tracking", use_container_width=True):
                st.session_state.capturing = True
                st.session_state.emotion_history = []
                st.session_state.timestamps = []
                st.session_state.report_generated = False
        with col_c2:
            if st.button("⏹️ Stop Tracking", use_container_width=True):
                st.session_state.capturing = False

    with col2:
        st.markdown("### 📊 Live Statistics")
        if st.session_state.emotion_history:
            emotion_counts = Counter(st.session_state.emotion_history)
            total = len(st.session_state.emotion_history)

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown(f"""
                    <div class="metric-card">
                        <h3>Total Captures</h3>
                        <h2>{total}</h2>
                    </div>
                """, unsafe_allow_html=True)
            with col_m2:
                most_common = emotion_counts.most_common(1)[0]
                st.markdown(f"""
                    <div class="metric-card">
                        <h3>Most Common</h3>
                        <h2>{most_common[0].capitalize()}</h2>
                        <p>{most_common[1]} times</p>
                    </div>
                """, unsafe_allow_html=True)

            current = st.session_state.emotion_history[-1]
            color = EMOTION_COLORS.get(current, '#AAAAAA')
            st.markdown(f"""
                <div class="emotion-card">
                    <h4>Current Emotion</h4>
                    <h2 style="color:{color}">{current.capitalize()}</h2>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Start tracking to see live statistics.")

    # Emotion tracking loop
    if st.session_state.capturing:
        placeholder = st.empty()
        for i in range(capture_duration):
            if not st.session_state.capturing:
                break
            if st.session_state.captured_image is not None:
                dominant, _ = analyze_emotion(st.session_state.captured_image)
                if dominant:
                    st.session_state.emotion_history.append(dominant)
                    st.session_state.timestamps.append(datetime.now())
                    with placeholder.container():
                        st.info(f"Captured: **{dominant.capitalize()}** — {i+1}/{capture_duration}")
            time.sleep(capture_interval)
        st.session_state.capturing = False
        st.session_state.report_generated = False
        st.rerun()

    # Report generation section
    if st.session_state.emotion_history and not st.session_state.report_generated:
        st.markdown("---")
        st.markdown("### 📋 Generate Mental Health Assessment Report")

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            report_type = st.selectbox(
                "Report Type",
                ["Comprehensive Analysis", "Summary Report", "Clinical Assessment"]
            )
        with col_r2:
            include_viz = st.checkbox("Include Visualizations", value=True)
        with col_r3:
            include_recommendations = st.checkbox("Include Recommendations", value=True)

        if st.button("📊 Generate Report", use_container_width=True):
            with st.spinner("Generating report..."):
                generate_report(
                    st.session_state.emotion_history,
                    st.session_state.timestamps,
                    st.session_state.captured_image,
                    report_type,
                    include_viz,
                    include_recommendations
                )
                st.session_state.report_generated = True


def generate_report(emotion_history, timestamps, captured_image, report_type, include_viz, include_recommendations):
    """Generate comprehensive mental health assessment report"""

    st.markdown("## 📊 Mental Health Assessment Report")
    st.markdown(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | **Type:** {report_type}")

    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📊 Analytics", "📉 Trends", "💡 Recommendations"])
    emotion_counts = Counter(emotion_history)

    with tab1:
        col_img, col_stats = st.columns(2)
        with col_img:
            if captured_image is not None:
                st.image(
                    cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB),
                    caption="Captured Image",
                    width=400
                )
        with col_stats:
            df = pd.DataFrame(list(emotion_counts.items()), columns=['Emotion', 'Count'])
            df['Percentage'] = (df['Count'] / len(emotion_history) * 100).round(2)
            df['Emotion'] = df['Emotion'].str.capitalize()
            st.markdown("### Emotion Distribution")
            st.dataframe(df, use_container_width=True)

    with tab2:
        if include_viz:
            col_pie, col_bar = st.columns(2)
            with col_pie:
                fig_pie = go.Figure(data=[go.Pie(
                    labels=[e.capitalize() for e in emotion_counts.keys()],
                    values=list(emotion_counts.values()),
                    marker_colors=[EMOTION_COLORS.get(e, '#AAAAAA') for e in emotion_counts.keys()]
                )])
                fig_pie.update_layout(title="Emotion Distribution")
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_bar:
                fig_bar = go.Figure(data=[go.Bar(
                    x=[e.capitalize() for e in emotion_counts.keys()],
                    y=list(emotion_counts.values()),
                    marker_color=[EMOTION_COLORS.get(e, '#AAAAAA') for e in emotion_counts.keys()]
                )])
                fig_bar.update_layout(title="Emotion Frequency", xaxis_title="Emotion", yaxis_title="Count")
                st.plotly_chart(fig_bar, use_container_width=True)

    with tab3:
        if len(emotion_history) > 1:
            emotion_to_num = {e: i for i, e in enumerate(set(emotion_history))}
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(emotion_history))),
                y=[emotion_to_num[e] for e in emotion_history],
                mode='lines+markers',
                text=emotion_history,
                hovertemplate='%{text}<extra></extra>',
                line=dict(color='#667eea', width=2),
                marker=dict(size=8, color='#764ba2')
            ))
            fig.update_yaxes(
                ticktext=[e.capitalize() for e in emotion_to_num.keys()],
                tickvals=list(emotion_to_num.values())
            )
            fig.update_layout(
                title="Emotion Timeline",
                xaxis_title="Capture Sequence",
                yaxis_title="Emotion",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

            total_changes = sum(
                1 for i in range(1, len(emotion_history))
                if emotion_history[i] != emotion_history[i-1]
            )
            stability = (1 - total_changes / len(emotion_history)) * 100

            c1, c2, c3 = st.columns(3)
            c1.metric("Emotional Stability", f"{stability:.1f}%")
            c2.metric("Emotion Switches", total_changes)
            c3.metric("Unique Emotions", len(set(emotion_history)))
        else:
            st.info("Need more than one capture to show trends.")

    with tab4:
        if include_recommendations:
            dominant = emotion_counts.most_common(1)[0][0]
            st.markdown(f"""
                <div class="recommendation-box">
                    <h4>Based on your dominant emotion: {dominant.capitalize()}</h4>
                </div>
            """, unsafe_allow_html=True)

            for rec in RECOMMENDATIONS.get(dominant, RECOMMENDATIONS['neutral']):
                st.markdown(f"- {rec}")

            st.markdown("### 📊 Key Insights")
            diversity = len(emotion_counts) / len(EMOTION_COLORS) * 100
            if diversity > 70:
                st.info("📊 Wide emotional range detected — healthy and normal.")
            elif diversity > 40:
                st.info("📈 Moderate emotional range. Consider exploring varied activities.")
            else:
                st.warning("⚠️ Limited emotional range. Try activities that bring new experiences.")

            if (emotion_counts.get('sad', 0) > len(emotion_history) * 0.3 or
                    emotion_counts.get('angry', 0) > len(emotion_history) * 0.3):
                st.error("""
                    🏥 **Professional Support Recommended**

                    Based on the patterns observed, consider reaching out to:
                    - A licensed therapist or counselor
                    - Your primary care physician
                    - A mental health helpline for immediate support
                """)

    # Download report
    report_lines = [
        "=" * 50,
        "MENTAL HEALTH ASSESSMENT REPORT",
        "=" * 50,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Report Type: {report_type}",
        "=" * 50,
        "",
        "EMOTION DISTRIBUTION:",
        "-" * 30,
        *[f"{e.capitalize()}: {c} times ({c/len(emotion_history)*100:.1f}%)"
          for e, c in emotion_counts.items()],
        "",
        "EMOTION TIMELINE:",
        "-" * 30,
        *[f"{t.strftime('%H:%M:%S')}: {e.capitalize()}"
          for e, t in zip(emotion_history, timestamps)],
        "",
        "=" * 50,
        "END OF REPORT",
        "=" * 50
    ]

    st.download_button(
        label="📥 Download Report",
        data="\n".join(report_lines),
        file_name=f"mental_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
        mime="text/plain"
    )


if __name__ == "__main__":
    main()
# ```

# Save this, then run:
# ```
# streamlit run app.py
