const AI_RECIPES = {
    'south': [
        { title: "Ragi Mudde with Sambar", prep: "20 mins", cals: "350 kcal", desc: "A nutrient-dense powerhouse of calcium and fiber from Karnataka.", ings: ["1 cup Ragi flour", "2 cups water", "Salt to taste", "1 tsp ghee"], steps: ["Boil water with salt & ghee.", "Gradually whisk in ragi flour.", "Cook on low flame until it forms a thick mass.", "Roll into a smooth ball. Serve hot."] },
        { title: "Kerala Fish Curry (Meen Curry)", prep: "40 mins", cals: "280 kcal", desc: "Omega-3 rich fish curry made with coconut and kokum.", ings: ["500g Seer fish", "1 cup Coconut milk", "Kokum", "Curry leaves, Mustard seeds"], steps: ["Temper spices in coconut oil.", "Add kokum and water, bring to boil.", "Add fish pieces and simmer until cooked.", "Stir in thick coconut milk."] },
        { title: "Andhra Gongura Pappu", prep: "30 mins", cals: "250 kcal", desc: "Iron-rich lentils with sorrel leaves.", ings: ["1 cup Toor dal", "2 cups Gongura leaves", "Green chilies", "Garlic"], steps: ["Pressure cook dal.", "Sauté gongura leaves with garlic.", "Mix with dal and temper with mustard seeds."] },
        { title: "Bisi Bele Bath", prep: "45 mins", cals: "400 kcal", desc: "Balanced meal of rice, lentils, and veggies.", ings: ["1 cup Rice", "1/2 cup Toor dal", "Mixed veggies", "Bisi bele bath powder"], steps: ["Cook rice and dal.", "Boil veggies with tamarind and spice powder.", "Mix everything and temper with ghee and cashews."] },
        { title: "Tamil Nadu Sundal", prep: "15 mins", cals: "180 kcal", desc: "High-protein chickpea snack.", ings: ["1 cup boiled Chickpeas", "Mustard seeds, urad dal", "Grated coconut", "Dry red chilies"], steps: ["Temper spices.", "Add boiled chickpeas and toss.", "Garnish with fresh coconut."] },
        { title: "Neer Dosa", prep: "20 mins", cals: "120 kcal", desc: "Light, lacy rice crepes from Mangalore.", ings: ["1 cup Rice (soaked)", "Salt", "Water"], steps: ["Grind rice into a thin watery batter.", "Pour onto a hot pan.", "Cover and cook for 1 min without flipping."] },
        { title: "Appam with Veg Stew", prep: "35 mins", cals: "260 kcal", desc: "Fermented rice pancake with coconut milk stew.", ings: ["Appam batter", "Mixed veggies", "Coconut milk", "Whole spices"], steps: ["Make appams in a curved pan.", "Simmer veggies in thin coconut milk with spices.", "Finish with thick coconut milk."] },
        { title: "Pesarattu (Moong Dal Dosa)", prep: "20 mins", cals: "200 kcal", desc: "Protein-packed Andhra breakfast.", ings: ["1 cup Green Moong (soaked)", "Ginger, green chilies", "Onions"], steps: ["Grind moong with ginger.", "Spread batter on a pan.", "Sprinkle onions, cook until crisp."] }
    ],
    'north': [
        { title: "Healthy Missi Roti", prep: "15 mins", cals: "200 kcal", desc: "High protein roti made with besan and whole wheat.", ings: ["1 cup besan", "1 cup whole wheat flour", "Onions, green chilies", "Ajwain, turmeric"], steps: ["Mix into a firm dough.", "Roll and cook on tawa.", "Brush lightly with ghee."] },
        { title: "Palak Paneer", prep: "30 mins", cals: "280 kcal", desc: "Iron and protein rich classic.", ings: ["2 cups Spinach puree", "200g Paneer cubes", "Garlic, ginger", "Garam masala"], steps: ["Blanch and puree spinach.", "Sauté aromatics.", "Add puree and paneer, simmer for 5 mins."] },
        { title: "Rajma Chawal (Portion Controlled)", prep: "45 mins", cals: "350 kcal", desc: "Fiber-rich kidney beans with rice.", ings: ["1 cup Rajma (soaked)", "Onion-tomato gravy", "1/2 cup brown rice"], steps: ["Pressure cook rajma.", "Simmer in spiced gravy.", "Serve with a measured portion of brown rice."] },
        { title: "Lauki Chana Dal", prep: "25 mins", cals: "180 kcal", desc: "Low-calorie bottle gourd with lentils.", ings: ["1 cup Lauki (cubed)", "1/2 cup Chana dal", "Turmeric, cumin"], steps: ["Pressure cook dal and lauki together.", "Temper with cumin and garlic."] },
        { title: "Baingan Bharta", prep: "35 mins", cals: "150 kcal", desc: "Smoky roasted eggplant mash.", ings: ["1 large Eggplant", "Onions, tomatoes", "Garlic, green chilies"], steps: ["Roast eggplant on open flame.", "Peel and mash.", "Sauté with aromatics and tomatoes."] },
        { title: "Multigrain Dal Paratha", prep: "20 mins", cals: "220 kcal", desc: "Leftover dal repurposed into a healthy flatbread.", ings: ["1 cup leftover thick Dal", "1 cup Multigrain flour", "Ajwain"], steps: ["Knead dal into the flour without water.", "Roll and cook on a tawa."] },
        { title: "Kashmiri Kahwa", prep: "10 mins", cals: "30 kcal", desc: "Antioxidant-rich green tea.", ings: ["Green tea leaves", "Saffron strands", "Cardamom, cinnamon", "Crushed almonds"], steps: ["Boil water with spices.", "Steep tea leaves.", "Serve with saffron and almonds."] },
        { title: "Tandoori Chicken Tikka", prep: "40 mins", cals: "250 kcal", desc: "Lean protein baked to perfection.", ings: ["250g Chicken breast", "Yogurt", "Tandoori masala"], steps: ["Marinate chicken in yogurt and spices.", "Bake or grill until cooked through."] }
    ],
    'east': [
        { title: "Steamed Fish (Bhapa Maach)", prep: "30 mins", cals: "280 kcal", desc: "Healthy Bengali classic.", ings: ["500g Fish", "2 tbsp Mustard paste", "Green chilies"], steps: ["Marinate fish in mustard paste.", "Place in a tiffin box.", "Steam for 20 minutes."] },
        { title: "Pakhala Bhata", prep: "10 mins", cals: "200 kcal", desc: "Fermented rice perfect for gut health.", ings: ["1 cup cooked rice", "Water, Curd", "Roasted cumin"], steps: ["Soak rice in water overnight.", "Mix with curd and roasted cumin."] },
        { title: "Dalma", prep: "30 mins", cals: "220 kcal", desc: "Odia lentil and vegetable stew.", ings: ["1 cup Toor dal", "Mixed veg (pumpkin, plantain)", "Panch phutana"], steps: ["Cook dal and veggies.", "Temper with panch phutana in ghee."] },
        { title: "Shukto", prep: "35 mins", cals: "190 kcal", desc: "Mild, bitter-sweet vegetable medley.", ings: ["Bitter gourd, plantain, sweet potato", "Mustard paste", "Milk"], steps: ["Fry veggies lightly.", "Simmer with mustard paste and milk."] },
        { title: "Chokha (Litti Chokha)", prep: "25 mins", cals: "150 kcal", desc: "Roasted vegetable mash.", ings: ["Roasted eggplant, tomato, potato", "Raw mustard oil", "Garlic, chilies"], steps: ["Mash roasted veggies.", "Mix with raw mustard oil and garlic."] },
        { title: "Macha Ghanta", prep: "45 mins", cals: "310 kcal", desc: "Fish head curry with mixed vegetables.", ings: ["Fried fish head", "Cabbage, potato, chana", "Garam masala"], steps: ["Cook veggies with spices.", "Add fried fish head and simmer."] },
        { title: "Chhena Poda (Low Sugar)", prep: "50 mins", cals: "250 kcal", desc: "Baked ricotta dessert.", ings: ["250g fresh Chhena", "Stevia/Jaggery", "Cardamom"], steps: ["Knead chhena with sweetener.", "Bake until top is caramelized."] }
    ],
    'west': [
        { title: "Sprouted Moong Usal", prep: "15 mins", cals: "220 kcal", desc: "Protein-packed Maharashtrian dish.", ings: ["2 cups sprouted moong", "Mustard seeds, curry leaves", "Onion, tomato"], steps: ["Temper spices.", "Saute aromatics.", "Add sprouts and cook."] },
        { title: "Bajra Raab", prep: "15 mins", cals: "180 kcal", desc: "Immunity boosting winter drink.", ings: ["2 tbsp Bajra flour", "Jaggery", "Ghee, Ajwain"], steps: ["Roast bajra in ghee.", "Add water and jaggery.", "Boil until thick."] },
        { title: "Gujarati Dal", prep: "25 mins", cals: "200 kcal", desc: "Sweet, sour, and spicy lentil soup.", ings: ["1 cup Toor dal", "Jaggery, Kokum", "Peanuts"], steps: ["Boil dal with peanuts.", "Add jaggery, kokum, and spices.", "Temper with mustard seeds."] },
        { title: "Methi Thepla", prep: "20 mins", cals: "160 kcal", desc: "Travel-friendly fenugreek flatbread.", ings: ["Whole wheat flour", "Fresh methi leaves", "Yogurt, spices"], steps: ["Knead into a dough.", "Roll into thin discs.", "Cook on tawa with minimal oil."] },
        { title: "Zunka Bhakar", prep: "20 mins", cals: "300 kcal", desc: "Besan curry with jowar roti.", ings: ["1 cup Besan", "Garlic, mustard seeds", "Jowar flour for bhakar"], steps: ["Make a thick besan curry (zunka).", "Serve with hot jowar bhakar."] },
        { title: "Khaman Dhokla", prep: "25 mins", cals: "150 kcal", desc: "Steamed, spongy gram flour snack.", ings: ["1 cup Besan", "Eno/Baking soda", "Curry leaves, green chilies"], steps: ["Prepare batter and steam.", "Pour tempered water over the dhokla."] },
        { title: "Thalipeeth", prep: "25 mins", cals: "220 kcal", desc: "Multigrain savory pancake.", ings: ["Bhajani flour (multigrain)", "Onions, coriander", "Sesame seeds"], steps: ["Form a dough.", "Pat onto a tawa with a hole in center.", "Cook until crisp."] }
    ],
    'diwali': [
        { title: "Sugar-Free Date & Almond Ladoo", prep: "15 mins", cals: "120 kcal", desc: "Guilt-free Diwali sweet.", ings: ["1 cup pitted dates", "1/2 cup almonds", "1 tbsp ghee"], steps: ["Roast nuts.", "Blend dates.", "Mix and roll into ladoos."] }
    ],
    'holi': [
        { title: "Baked Gujiya", prep: "40 mins", cals: "180 kcal", desc: "Avoid deep-frying with this baked alternative.", ings: ["Whole wheat flour", "Mawa", "Stevia"], steps: ["Prepare stuffing.", "Roll pastry, fill, seal.", "Bake at 180°C for 20 mins."] }
    ],
    'eid': [
        { title: "Quinoa Chicken Biryani", prep: "45 mins", cals: "350 kcal", desc: "High-protein, low-GI alternative.", ings: ["1 cup Quinoa", "300g Chicken", "Biryani spices"], steps: ["Marinate & cook chicken.", "Layer with cooked quinoa.", "Dum for 10 mins."] }
    ],
    'pongal': [
        { title: "Millet Sweet Pongal", prep: "30 mins", cals: "250 kcal", desc: "Swap white rice for Foxtail Millet.", ings: ["1/2 cup Foxtail Millet", "1/4 cup Moong dal", "Jaggery"], steps: ["Roast dal and cook with millet.", "Stir in jaggery syrup.", "Garnish with cashews."] }
    ]
};
