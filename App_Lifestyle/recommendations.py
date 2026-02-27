"""
Cycle-synced lifestyle recommendations engine.
Provides personalized exercise, nutrition, self-care, and pain management
recommendations based on the user's current menstrual cycle phase.
"""

RECOMMENDATIONS = {
    'menstrual': {
        'phase_name': 'Menstrual Phase',
        'phase_emoji': 'Period Days',
        'color': '#e74c3c',
        'summary': 'Your body is working hard. Honor it with rest, warmth, and nourishing foods. Pain management is the priority.',
        'pain_relief': [
            {
                'title': 'Heat Therapy',
                'desc': 'Apply a heating pad or hot water bottle to your lower abdomen for 15-20 minutes. Heat increases blood flow and relaxes the uterine muscles causing cramps. Studies show heat therapy is as effective as ibuprofen for menstrual pain.',
                'icon': 'fas fa-fire',
            },
            {
                'title': 'Magnesium Supplementation',
                'desc': 'Magnesium helps relax smooth muscle tissue. Try magnesium-rich foods (dark chocolate, almonds, bananas) or a supplement. Start a few days before your expected period for best results.',
                'icon': 'fas fa-capsules',
            },
            {
                'title': 'TENS Device',
                'desc': 'Transcutaneous Electrical Nerve Stimulation (TENS) can block pain signals. Small, affordable devices can be worn discreetly throughout the day.',
                'icon': 'fas fa-bolt',
            },
            {
                'title': 'Acupressure Points',
                'desc': 'Press the point 4 finger-widths above your inner ankle bone (SP6) for 5 minutes on each side. This traditional technique can ease cramps and lower back pain.',
                'icon': 'fas fa-hand-point-up',
            },
        ],
        'exercise': [
            {
                'title': 'Gentle Yoga',
                'desc': 'Try Child\'s Pose, Cat-Cow, Supine Twist, and Reclined Butterfly. These poses ease cramps by gently stretching the pelvic area. Avoid inversions if uncomfortable.',
                'icon': 'fas fa-pray',
            },
            {
                'title': 'Light Walking',
                'desc': '15-20 minutes of walking releases endorphins (natural painkillers) and reduces bloating. Don\'t push intensity - listen to your body.',
                'icon': 'fas fa-walking',
            },
            {
                'title': 'Stretching',
                'desc': 'Gentle lower back stretches, hip openers, and hamstring stretches can significantly reduce period pain and stiffness.',
                'icon': 'fas fa-child',
            },
        ],
        'nutrition': [
            {
                'title': 'Anti-Inflammatory Foods',
                'desc': 'Focus on: ginger tea (reduces prostaglandins causing cramps), turmeric, salmon, walnuts, berries, and leafy greens. Avoid excessive salt (bloating), caffeine (worsens cramps), and alcohol.',
                'icon': 'fas fa-leaf',
            },
            {
                'title': 'Iron-Rich Foods',
                'desc': 'You\'re losing iron through menstrual blood. Eat spinach, red meat, lentils, fortified cereals, and pair with vitamin C (citrus) for better absorption.',
                'icon': 'fas fa-drumstick-bite',
            },
            {
                'title': 'Warm Liquids',
                'desc': 'Warm water, ginger tea, chamomile tea, and bone broth help relax muscles and ease cramping. Avoid ice-cold drinks which can increase cramping.',
                'icon': 'fas fa-mug-hot',
            },
        ],
        'self_care': [
            {
                'title': 'Warm Bath with Epsom Salt',
                'desc': 'Magnesium in Epsom salt absorbs through skin, relaxing muscles. Add lavender essential oil for calming effects. 20 minutes is ideal.',
                'icon': 'fas fa-bath',
            },
            {
                'title': 'Permission to Rest',
                'desc': 'This is not laziness - it\'s biology. Your body is doing extraordinary work. Cancel non-essential commitments if you need to. Rest is productive.',
                'icon': 'fas fa-couch',
            },
            {
                'title': 'Comfort Toolkit',
                'desc': 'Prepare your kit: heating pad, comfortable clothes, herbal tea, dark chocolate, and a good book or show. Having supplies ready reduces stress.',
                'icon': 'fas fa-first-aid',
            },
        ],
    },
    'follicular': {
        'phase_name': 'Follicular Phase',
        'phase_emoji': 'Rising Energy',
        'color': '#2ecc71',
        'summary': 'Energy and estrogen are rising! This is your power phase. Great time to challenge yourself and build pain resilience for next cycle.',
        'pain_relief': [
            {
                'title': 'Prevention Mode',
                'desc': 'Use this high-energy phase to strengthen your core and pelvic floor. Stronger muscles = less severe cramps next cycle. Regular exercise during this phase reduces future period pain by up to 25%.',
                'icon': 'fas fa-shield-alt',
            },
        ],
        'exercise': [
            {
                'title': 'High-Intensity Training',
                'desc': 'Your body can handle more now! HIIT, running, cycling, strength training - push your limits. Estrogen supports muscle recovery and performance.',
                'icon': 'fas fa-running',
            },
            {
                'title': 'Try Something New',
                'desc': 'Brain plasticity is higher. Great time to learn a new sport, dance class, or exercise routine.',
                'icon': 'fas fa-star',
            },
            {
                'title': 'Strength Training',
                'desc': 'Build muscle more efficiently during this phase. Focus on compound movements: squats, deadlifts, push-ups.',
                'icon': 'fas fa-dumbbell',
            },
        ],
        'nutrition': [
            {
                'title': 'Protein-Rich Foods',
                'desc': 'Support muscle growth with lean meats, eggs, legumes, and tofu. Your metabolism is efficient now.',
                'icon': 'fas fa-egg',
            },
            {
                'title': 'Fermented Foods',
                'desc': 'Support gut health with yogurt, kimchi, sauerkraut. Gut health directly impacts hormonal balance and future pain levels.',
                'icon': 'fas fa-seedling',
            },
        ],
        'self_care': [
            {
                'title': 'Social Connection',
                'desc': 'You\'re naturally more outgoing now. Schedule social activities, networking, and meaningful conversations.',
                'icon': 'fas fa-users',
            },
            {
                'title': 'Set Goals',
                'desc': 'Mental clarity is high. Plan projects, have important conversations, make decisions. Your brain is at peak performance.',
                'icon': 'fas fa-bullseye',
            },
        ],
    },
    'ovulation': {
        'phase_name': 'Ovulation Phase',
        'phase_emoji': 'Peak Energy',
        'color': '#f39c12',
        'summary': 'You\'re at peak energy, confidence, and communication skills. Make the most of this short window!',
        'pain_relief': [
            {
                'title': 'Ovulation Pain (Mittelschmerz)',
                'desc': 'Some women feel mild one-sided pain during ovulation. This is normal and usually passes in hours. Light heat or a warm drink can help.',
                'icon': 'fas fa-info-circle',
            },
        ],
        'exercise': [
            {
                'title': 'Peak Performance',
                'desc': 'Your strength and endurance peak around ovulation. Set personal records, compete, give maximum effort.',
                'icon': 'fas fa-trophy',
            },
            {
                'title': 'Group Activities',
                'desc': 'Social energy is high. Team sports, group fitness classes, hiking with friends.',
                'icon': 'fas fa-people-carry',
            },
        ],
        'nutrition': [
            {
                'title': 'Lighter Meals',
                'desc': 'Appetite often decreases naturally. Focus on fresh vegetables, fruits, whole grains, and lean proteins.',
                'icon': 'fas fa-salad',
            },
            {
                'title': 'Liver-Supporting Foods',
                'desc': 'Help your liver metabolize the estrogen surge: cruciferous vegetables (broccoli, cauliflower, Brussels sprouts), garlic, and citrus.',
                'icon': 'fas fa-lemon',
            },
        ],
        'self_care': [
            {
                'title': 'Important Conversations',
                'desc': 'Communication skills peak during ovulation. Schedule job interviews, difficult conversations, presentations, and date nights.',
                'icon': 'fas fa-comments',
            },
        ],
    },
    'luteal': {
        'phase_name': 'Luteal Phase',
        'phase_emoji': 'Wind Down',
        'color': '#9b59b6',
        'summary': 'Progesterone rises, energy starts to dip. Time to prepare for your period and proactively manage upcoming pain.',
        'pain_relief': [
            {
                'title': 'Pre-Period Pain Prevention',
                'desc': 'Start taking calcium (1000mg/day) and vitamin B6 now. Studies show these reduce PMS severity by up to 50% when taken during the luteal phase.',
                'icon': 'fas fa-prescription-bottle',
            },
            {
                'title': 'Reduce Inflammation Now',
                'desc': 'Cut back on refined sugar, alcohol, and processed foods. Add omega-3 fatty acids (fish oil, flaxseed, walnuts). What you eat now determines how painful your period will be.',
                'icon': 'fas fa-ban',
            },
            {
                'title': 'Start Gentle Movement',
                'desc': 'Regular light exercise in the luteal phase significantly reduces upcoming period pain. Even 20 minutes of walking daily makes a difference.',
                'icon': 'fas fa-heartbeat',
            },
        ],
        'exercise': [
            {
                'title': 'Moderate Intensity',
                'desc': 'Scale back from peak efforts. Pilates, moderate yoga, swimming, and steady-state cardio are ideal.',
                'icon': 'fas fa-swimmer',
            },
            {
                'title': 'Pelvic Floor Exercises',
                'desc': 'Kegel exercises and pelvic floor work can reduce period pain. Practice daily during this phase.',
                'icon': 'fas fa-circle-notch',
            },
        ],
        'nutrition': [
            {
                'title': 'Complex Carbohydrates',
                'desc': 'Serotonin drops before your period, causing cravings. Satisfy them with whole grains, sweet potatoes, oats - not refined sugar which worsens mood swings.',
                'icon': 'fas fa-bread-slice',
            },
            {
                'title': 'Reduce Salt & Caffeine',
                'desc': 'Both worsen bloating and breast tenderness. Switch to herbal teas (chamomile, peppermint). Limit coffee to 1 cup.',
                'icon': 'fas fa-coffee',
            },
            {
                'title': 'Dark Chocolate (Yes!)',
                'desc': '1-2 squares of dark chocolate (70%+) provides magnesium and triggers endorphin release. A legitimate PMS remedy!',
                'icon': 'fas fa-cookie',
            },
        ],
        'self_care': [
            {
                'title': 'Stress Management',
                'desc': 'Cortisol amplifies PMS symptoms and pain. Journaling, meditation, deep breathing, or a warm bath can lower cortisol significantly.',
                'icon': 'fas fa-spa',
            },
            {
                'title': 'Sleep Priority',
                'desc': 'You need more sleep now. Aim for 8-9 hours. Poor sleep worsens PMS, pain, and mood. Create a relaxing bedtime routine.',
                'icon': 'fas fa-moon',
            },
            {
                'title': 'Prepare Your Period Kit',
                'desc': 'Stock up on supplies: pads/tampons, heating pad, comfort foods, pain medication, herbal tea. Being prepared reduces anxiety about your upcoming period.',
                'icon': 'fas fa-box-open',
            },
        ],
    },
}


def get_all_recommendations(phase_key):
    """Get recommendations for the given phase. Falls back to menstrual if unknown."""
    if phase_key and phase_key in RECOMMENDATIONS:
        return RECOMMENDATIONS[phase_key]
    return None


def get_recommendations_by_category(phase_key, category):
    """Get recommendations for a specific category in the given phase."""
    recs = get_all_recommendations(phase_key)
    if recs and category in recs:
        return recs[category]
    return []
