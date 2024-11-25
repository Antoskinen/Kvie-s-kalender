import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date, timedelta
import json
import os
import locale

# Danish month and day names
MONTHS_DA = {
    1: "Januar", 2: "Februar", 3: "Marts", 4: "April",
    5: "Maj", 6: "Juni", 7: "Juli", 8: "August",
    9: "September", 10: "Oktober", 11: "November", 12: "December"
}

DAYS_DA = ["Man", "Tir", "Ons", "Tor", "Fre", "Lør", "Søn"]

# Set page config
st.set_page_config(page_title="Kvie sø kalender 2025", layout="wide")

# Initialize session state for bookings and selected dates
if 'bookings' not in st.session_state:
    st.session_state.bookings = {}
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'end_date' not in st.session_state:
    st.session_state.end_date = None

# Function to save bookings to file
def save_bookings():
    with open('bookings.json', 'w') as f:
        json.dump(st.session_state.bookings, f)

# Function to load bookings from file
def load_bookings():
    if os.path.exists('bookings.json'):
        try:
            with open('bookings.json', 'r') as f:
                bookings = json.load(f)
                # Convert old format to new format if necessary
                for date_str, booking in bookings.items():
                    if 'range_start' not in booking:
                        booking['range_start'] = date_str
                        booking['range_end'] = date_str
                st.session_state.bookings = bookings
        except Exception as e:
            st.error(f"Fejl ved indlæsning af bookinger: {e}")
            st.session_state.bookings = {}

# Function to get all dates in a range
def get_date_range(start_date, end_date):
    if not start_date or not end_date:
        return []
    
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)
    return dates

# Function to format date in Danish
def format_date_danish(date_obj):
    if isinstance(date_obj, str):
        date_obj = datetime.strptime(date_obj, "%Y-%m-%d").date()
    return date_obj.strftime("%d-%m-%Y")

# Function to check if a date is in any booked range
def is_date_booked(date_str):
    return date_str in st.session_state.bookings

# Function to check if date is in current selection range
def is_date_in_selection(date_str):
    if not st.session_state.start_date or not st.session_state.end_date:
        return False
    
    current_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return st.session_state.start_date <= current_date <= st.session_state.end_date

# Load existing bookings
load_bookings()

# Title
st.title("Kvie sø kalender 2025")

# Create sidebar for booking details
st.sidebar.header("Vælg Datoer")

# Month selection
selected_month = st.sidebar.selectbox(
    "Vælg Måned",
    range(1, 13),
    format_func=lambda x: MONTHS_DA[x]
)

# Date range selection
start_date = st.sidebar.date_input(
    "Startdato",
    min_value=date(2025, 1, 1),
    max_value=date(2025, 12, 31),
    value=st.session_state.start_date if st.session_state.start_date else None
)

end_date = st.sidebar.date_input(
    "Slutdato",
    min_value=date(2025, 1, 1),
    max_value=date(2025, 12, 31),
    value=st.session_state.end_date if st.session_state.end_date else None
)

# Update session state
st.session_state.start_date = start_date
st.session_state.end_date = end_date

# Booking details
st.sidebar.header("Bookingdetaljer")
booking_name = st.sidebar.text_input("Navn")
booking_description = st.sidebar.text_area("Beskrivelse")

# Submit button for date range
if st.sidebar.button("Book Datoer"):
    if booking_name and booking_description and start_date and end_date:
        if start_date > end_date:
            st.sidebar.error("Slutdato skal være efter startdato")
        else:
            # Check for booking conflicts
            date_range = get_date_range(start_date, end_date)
            conflicts = [date_str for date_str in date_range if is_date_booked(date_str)]
            
            if conflicts:
                st.sidebar.error(f"Booking konflikt på datoerne: {', '.join(map(format_date_danish, conflicts))}")
            else:
                # Book all dates in range
                for date_str in date_range:
                    st.session_state.bookings[date_str] = {
                        "name": booking_name,
                        "description": booking_description,
                        "range_start": start_date.strftime("%Y-%m-%d"),
                        "range_end": end_date.strftime("%Y-%m-%d")
                    }
                save_bookings()
                st.sidebar.success(f"Booket {len(date_range)} dage")
                # Clear selection
                st.session_state.start_date = None
                st.session_state.end_date = None
                st.rerun()
    else:
        st.sidebar.error("Udfyld venligst alle felter og vælg et datointerval")

# Create main calendar view
st.header(f"Kalender - {MONTHS_DA[selected_month]} 2025")

# Get calendar for selected month
cal = calendar.monthcalendar(2025, selected_month)

# Create calendar display
cols = st.columns(7)

# Display week days
for i, day in enumerate(DAYS_DA):
    cols[i].markdown(f"**{day}**")

# Display calendar dates
for week in cal:
    cols = st.columns(7)
    for idx, day in enumerate(week):
        if day != 0:
            date_str = date(2025, selected_month, day).strftime("%Y-%m-%d")
            
            # Style based on booking status and selection
            if is_date_booked(date_str):
                booking = st.session_state.bookings[date_str]
                cols[idx].markdown(
                    f"<div style='padding: 10px; background-color: #ffcccc; border-radius: 5px;'>"
                    f"<strong>{day}</strong> 📅<br>"
                    f"<small>{booking['name']}</small></div>",
                    unsafe_allow_html=True
                )
            elif is_date_in_selection(date_str):
                cols[idx].markdown(
                    f"<div style='padding: 10px; background-color: #ccffcc; border-radius: 5px;'>"
                    f"<strong>{day}</strong> ✓</div>",
                    unsafe_allow_html=True
                )
            else:
                cols[idx].markdown(f"<div style='padding: 10px;'>{day}</div>", unsafe_allow_html=True)
        else:
            cols[idx].markdown("")

# Display bookings
st.header("Nuværende Bookinger")
if st.session_state.bookings:
    # Create a dictionary to store unique ranges
    unique_ranges = {}
    
    # Group bookings by range
    for date_str, booking in st.session_state.bookings.items():
        range_key = f"{format_date_danish(booking['range_start'])} til {format_date_danish(booking['range_end'])}"
        if range_key not in unique_ranges:
            unique_ranges[range_key] = booking

    # Display unique ranges
    for range_key, booking in unique_ranges.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{range_key}** - {booking['name']}")
            st.markdown(f"> {booking['description']}")
        with col2:
            if st.button(f"Slet booking", key=f"del_{range_key}"):
                # Remove all dates in this range
                st.session_state.bookings = {
                    k: v for k, v in st.session_state.bookings.items()
                    if v['range_start'] != booking['range_start'] or v['range_end'] != booking['range_end']
                }
                save_bookings()
                st.rerun()
else:
    st.info("Ingen bookinger endnu")

# Display selected range
if st.session_state.start_date and st.session_state.end_date:
    st.header("Valgt Interval")
    st.write(f"Fra: {format_date_danish(st.session_state.start_date)}")
    st.write(f"Til: {format_date_danish(st.session_state.end_date)}")
    st.write(f"Antal dage: {(st.session_state.end_date - st.session_state.start_date).days + 1}")
