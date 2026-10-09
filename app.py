import streamlit as st  # Imports Streamlit so we can create the controls, messages, and webpage

GRAVITY = 9.81  # Gravitational acceleration in meters per second squared
BEAM_LENGTH = 0.50  # The beam extends from 0.00 meters to 0.50 meters

COINS_BY_COUNTRY = {  # Organizes coin masses by country
    "United States": {
        "Penny": 2.500,
        "Nickel": 5.000,
        "Dime": 2.268,
        "Quarter": 5.670,
        "Half dollar": 11.340,
        "Dollar coin": 8.100,
    },

    "Euro area": {
        "1 cent": 2.300,
        "2 cents": 3.060,
        "5 cents": 3.920,
        "10 cents": 4.100,
        "20 cents": 5.740,
        "50 cents": 7.800,
        "1 euro": 7.500,
        "2 euros": 8.500,
    },

    "United Kingdom": {
        "1 penny": 3.560,
        "2 pence": 7.120,
        "5 pence": 3.250,
        "10 pence": 6.500,
        "20 pence": 5.000,
        "50 pence": 8.000,
        "1 pound": 9.500,
        "2 pounds": 12.000,
    },

    "Japan": {
        "1 yen": 1.000,
        "5 yen": 3.750,
        "10 yen": 4.500,
        "50 yen": 4.000,
        "100 yen": 4.800,
        "500 yen": 7.100,
    },
}


def calculate_torque(mass_grams, position, pivot):  # Calculates the torque produced by one mass
    mass_kg = mass_grams / 1000  # Converts grams to kilograms
    distance = abs(position - pivot)  # Finds the positive distance between the mass and pivot
    force = mass_kg * GRAVITY  # Calculates weight using force = mass × gravity
    torque = distance * force  # Calculates torque using torque = distance × force

    if position < pivot:  # Left of the pivot produces positive counterclockwise torque
        return torque
    elif position > pivot:  # Right of the pivot produces negative clockwise torque
        return -torque
    else:
        return 0  # A mass directly on the pivot produces no torque


def find_equilibrium_position(masses, pivot, solve_index):  # Finds where one mass must be placed for equilibrium
    target_mass = masses[solve_index][0]  # Gets the selected mass

    if target_mass == 0:  # A zero-gram mass cannot balance the beam
        return None

    other_moments = sum(  # Adds the moments from every mass except the selected mass
        mass * (pivot - position)
        for index, (mass, position) in enumerate(masses)
        if index != solve_index
    )

    return pivot + other_moments / target_mass  # Rearranges the equilibrium equation to find the position


def draw_beam(masses, pivot):  # Creates the SVG beam visualization
    width = 760  # Internal width of the drawing
    beam_left = 45  # Left margin
    beam_right = width - 45  # Right margin
    beam_y = 170  # Vertical position of the beam

    colors = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"]  # Colors used for the masses

    def x_position(position):  # Converts a position in meters into an SVG screen coordinate
        return beam_left + (position / BEAM_LENGTH) * (beam_right - beam_left)

    mass_shapes = []  # Stores the SVG drawing instructions for every mass

    for index, (mass, position) in enumerate(masses, start=1):
        if position is None:  # Skips an unknown position until the solver calculates it
            continue

        x = x_position(position)  # Finds the horizontal drawing location
        color = colors[(index - 1) % len(colors)]  # Repeats colors when there are more than five masses

        mass_shapes.append(
            f'<line x1="{x:.1f}" y1="{beam_y}" x2="{x:.1f}" y2="105" stroke="{color}" stroke-width="3" />'
            f'<circle cx="{x:.1f}" cy="88" r="17" fill="{color}" />'
            f'<text x="{x:.1f}" y="93" text-anchor="middle" fill="white" font-size="12" font-weight="bold">{index}</text>'
            f'<text x="{x:.1f}" y="57" text-anchor="middle" fill="#334155" font-size="12">{mass:g} g</text>'
        )

    pivot_x = x_position(pivot)  # Converts the pivot position into an SVG coordinate

    return f"""
    <svg viewBox="0 0 {width} 245" width="100%" role="img" aria-label="Beam with masses and pivot">
        <rect x="{beam_left}" y="{beam_y - 7}" width="{beam_right - beam_left}" height="14" rx="7" fill="#64748b" />

        {''.join(mass_shapes)}

        <polygon points="{pivot_x:.1f},{beam_y + 8} {pivot_x - 25:.1f},220 {pivot_x + 25:.1f},220" fill="#0f172a" />

        <text x="{pivot_x:.1f}" y="239" text-anchor="middle" fill="#334155" font-size="12">
            pivot: {pivot:.2f} m
        </text>

        <text x="{beam_left}" y="201" text-anchor="middle" fill="#64748b" font-size="11">
            0.00 m
        </text>

        <text x="{beam_right}" y="201" text-anchor="middle" fill="#64748b" font-size="11">
            {BEAM_LENGTH:.2f} m
        </text>
    </svg>
    """


st.title("Torque Balance Simulator")  # Main webpage heading

st.write(
    "Add masses to a beam and see whether the system is balanced, "
    "rotates clockwise, or rotates counter-clockwise."
)

pivot = st.number_input(
    "Pivot position (m)",
    min_value=0.0,
    max_value=BEAM_LENGTH,
    value=0.25,
    step=0.01,
)  # Lets the user move the pivot

number_of_masses = st.slider(
    "Number of masses",
    min_value=1,
    max_value=10,
    value=2,
)  # Controls the number of mass sections

solve_mode = st.checkbox(
    "Solve for an equilibrium position"
)  # Turns the equilibrium solver on or off

solve_mass_number = None  # Stores the visible number of the mass being solved

if solve_mode:
    solve_mass_number = st.selectbox(
        "Mass whose position should be solved",
        range(1, number_of_masses + 1),
        format_func=lambda number: f"Mass {number}",
    )


masses = []  # Stores every mass and position

for number in range(1, number_of_masses + 1):
    st.subheader(f"Mass {number}")

    mass_source = st.selectbox(
        f"Mass {number} source",
        ["Custom mass", "Coin"],
        key=f"mass_source_{number}",
    )  # Lets the user select a custom mass or coin

    if mass_source == "Custom mass":
        mass = st.number_input(
            f"Mass {number} (g)",
            min_value=0.0,
            value=10.0,
            step=1.0,
            key=f"mass_{number}",
        )  # Allows the user to enter any mass in grams

    else:
        country = st.selectbox(
            f"Country for Mass {number}",
            list(COINS_BY_COUNTRY.keys()),
            key=f"country_{number}",
        )  # Selects the coin's country

        coin_name = st.selectbox(
            f"Coin for Mass {number}",
            list(COINS_BY_COUNTRY[country].keys()),
            key=f"coin_{number}",
        )  # Displays only coins from the selected country

        coin_count = st.number_input(
            f"Number of {coin_name} coins",
            min_value=1,
            max_value=100,
            value=1,
            step=1,
            key=f"coin_count_{number}",
        )  # Allows multiple identical coins

        one_coin_mass = COINS_BY_COUNTRY[country][coin_name]  # Gets the mass of one selected coin
        mass = one_coin_mass * coin_count  # Calculates the combined mass

        st.caption(
            f"{country} — {coin_name}: "
            f"{one_coin_mass:.3f} g each, "
            f"{mass:.3f} g total"
        )

    if solve_mode and number == solve_mass_number:
        position = None  # Marks this position as unknown
        st.caption("This position will be calculated below.")

    else:
        position = st.number_input(
            f"Position {number} (m)",
            min_value=0.0,
            max_value=BEAM_LENGTH,
            value=0.10 if number % 2 == 1 else 0.40,
            step=0.01,
            key=f"position_{number}",
        )

    masses.append([mass, position])  # Saves the completed mass entry


solution_error = None  # Holds an error message if no usable solution exists

if solve_mode:
    solve_index = solve_mass_number - 1  # Converts the visible mass number into a Python list index

    solved_position = find_equilibrium_position(
        masses,
        pivot,
        solve_index,
    )

    if solved_position is None:
        solution_error = "The selected mass must be greater than zero."

    elif not 0 <= solved_position <= BEAM_LENGTH:
        solution_error = (
            f"Equilibrium would require {solved_position:.3f} m, "
            f"which is outside the {BEAM_LENGTH:.2f} m beam. "
            f"Try a heavier mass or move another mass."
        )

    else:
        masses[solve_index][1] = solved_position  # Inserts the calculated position

        st.success(
            f"Place Mass {solve_mass_number} at "
            f"{solved_position:.3f} m for equilibrium."
        )


st.subheader("Beam visualization")

st.markdown(
    draw_beam(masses, pivot),
    unsafe_allow_html=True,
)  # Displays the SVG beam

st.caption(
    "Each numbered circle is a mass. "
    "Change any input above and the diagram updates automatically."
)


if solution_error:
    st.error(solution_error)
    st.stop()  # Stops because the selected mass does not have a valid position


net_torque = 0  # Starts the total torque at zero

st.subheader("Results")

for number, (mass, position) in enumerate(masses, start=1):
    torque = calculate_torque(
        mass,
        position,
        pivot,
    )

    net_torque += torque  # Adds this mass's torque to the total

    st.write(
        f"Mass {number}: **{torque:.4f} N·m**"
    )


st.metric(
    "Net Torque",
    f"{net_torque:.4f} N·m",
)

tolerance = 0.005  # Torques closer to zero than this are treated as approximately balanced

if abs(net_torque) < tolerance:
    st.success(
        "System is approximately in equilibrium."
    )

elif net_torque > 0:
    st.warning(
        "System will rotate counter-clockwise."
    )

else:
    st.warning(
        "System will rotate clockwise."
    )


st.caption(
    "Coin masses should be checked against the official mint or "
    "central bank for each country. U.S. specifications: "
    "https://www.usmint.gov/learn/coins-and-medals/"
    "circulating-coins/coin-specifications.html"
)
