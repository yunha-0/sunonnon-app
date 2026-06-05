import math
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='단위원을 통해 알아보는 sin함수와 cos함수',
    page_icon=':abcd:'
)

st.title('단위원을 통해 알아보는 sin함수와 cos함수')
st.write('왼쪽에는 단위원을, 오른쪽에는 사인함수와 코사인함수를 나타내는 좌표평면을 표시합니다.')

angles = [math.radians(deg) for deg in range(0, 361)]
values = {
    'angle': angles,
    'sin': [math.sin(angle) for angle in angles],
    'cos': [math.cos(angle) for angle in angles],
}

df = pd.DataFrame(values)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('단위원(unit circle)')

    fig, ax = plt.subplots(figsize=(4, 4))
    circle = plt.Circle((0, 0), 1, fill=False, linewidth=2, color='black')
    ax.add_patch(circle)
    ax.axhline(0, color='gray', linewidth=0.8)
    ax.axvline(0, color='gray', linewidth=0.8)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title('단위원')
    st.pyplot(fig)

with col2:
    st.subheader('사인함수와 코사인함수')

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(df['angle'], df['sin'], label='sin(x)', color='#1f77b4')
    ax2.plot(df['angle'], df['cos'], label='cos(x)', color='#ff7f0e')
    ax2.set_xlabel('각도 (rad)')
    ax2.set_ylabel('값')
    ax2.set_title('사인함수와 코사인함수')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig2)
