import math
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title='단위원을 통해 알아보는 sin함수와 cos함수',
    page_icon=':abcd:'
)

st.title('단위원을 통해 알아보는 sin함수와 코사인함수')
st.write('왼쪽에는 단위원을, 오른쪽에는 사인함수와 코사인함수를 나타내는 좌표평면을 표시합니다.')

angles = [math.radians(deg) for deg in range(0, 361)]
unit_circle = pd.DataFrame({
    'x': [math.cos(angle) for angle in angles],
    'y': [math.sin(angle) for angle in angles],
})

trig_data = pd.DataFrame({
    'angle': angles * 2,
    'value': [math.sin(angle) for angle in angles] + [math.cos(angle) for angle in angles],
    'function': ['sin'] * len(angles) + ['cos'] * len(angles),
})

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader('단위원(unit circle)')

    circle_chart = alt.Chart(unit_circle).mark_line(color='black').encode(
        x=alt.X('x:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=alt.Axis(title='x')),
        y=alt.Y('y:Q', scale=alt.Scale(domain=[-1.2, 1.2]), axis=alt.Axis(title='y')),
    ).properties(width=350, height=350)

    x_axis = alt.Chart(pd.DataFrame({'x': [-1.2, 1.2], 'y': [0, 0]})).mark_rule(color='gray')
    y_axis = alt.Chart(pd.DataFrame({'x': [0, 0], 'y': [-1.2, 1.2]})).mark_rule(color='gray')

    st.altair_chart(alt.layer(circle_chart, x_axis, y_axis), use_container_width=True)

with col2:
    st.subheader('사인함수와 코사인함수')

    line_chart = alt.Chart(trig_data).mark_line().encode(
        x=alt.X('angle:Q', title='각도 (rad)'),
        y=alt.Y('value:Q', title='값'),
        color=alt.Color('function:N', title='함수'),
    ).properties(width=500, height=350)

    st.altair_chart(line_chart, use_container_width=True)
