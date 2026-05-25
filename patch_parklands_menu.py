#!/usr/bin/env python3
"""Phase 1B — Parklands menu flagship upgrade."""
import re
from pathlib import Path

ROOT = Path(__file__).parent
MENU = ROOT / "parklands" / "menu.html"
PHOTOS = ROOT / "assets" / "js" / "menu-photos.js"

NEW_SECTIONS = r'''


  <details class="menu-accordion" name="menu-groups" id="fuyong" itemscope itemtype="https://schema.org/MenuSection">
    <summary class="accordion-trigger">
      <span class="accordion-title" itemprop="name">FuYong</span>
      <span class="accordion-badge">5 Dishes</span>
    </summary>
    <ul class="accordion-panel-list" role="list">
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Mushroom FuYong</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="800">800</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">A Chinese omelette with mushrooms — soft, savoury, and enriched with wok technique. A quiet classic.</span>
  <div class="item-order-row">
    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Mushroom FuYong from Mister Wok Parklands">Order</button>
  </div>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Chicken FuYong</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="800">800</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Shredded chicken folded into a soft wok omelette. Protein-rich, delicate in texture, and deeply familiar.</span>
  <div class="item-order-row">
    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Chicken FuYong from Mister Wok Parklands">Order</button>
  </div>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Chicken and Mushroom FuYong</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="850">850</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Chicken and mushroom together in a wok omelette — earthy and savoury, with a satisfying finish.</span>
  <div class="item-order-row">
    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Chicken and Mushroom FuYong from Mister Wok Parklands">Order</button>
  </div>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Beef and Mushroom FuYong</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="850">850</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Tender beef strips and mushroom in a soft wok omelette. Hearty and quietly confident.</span>
  <div class="item-order-row">
    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Beef and Mushroom FuYong from Mister Wok Parklands">Order</button>
  </div>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Prawn and Mushroom FuYong</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="1200">1,200</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Prawn and mushroom in a delicate wok omelette. The premium FuYong — sweet prawn, earthy mushroom, silky egg.</span>
  <div class="item-order-row">
    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Prawn and Mushroom FuYong from Mister Wok Parklands">Order</button>
  </div>
</li>
    </ul>
  </details>
  <details class="menu-accordion" name="menu-groups" id="desserts" itemscope itemtype="https://schema.org/MenuSection">
    <summary class="accordion-trigger">
      <span class="accordion-title" itemprop="name">Desserts</span>
      <span class="accordion-badge">8 Dishes</span>
    </summary>
    <ul class="accordion-panel-list" role="list">
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Ice Cream Delight Special</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="500">500</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Vanilla, strawberry or chocolate. Three scoops, one decision — the simplest ending to a great meal.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Date Pancakes With Ice Cream</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="650">650</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Warm date pancakes served with a scoop of ice cream. Sticky, sweet, and deeply satisfying.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Toffee Banana With Ice Cream</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="650">650</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Banana in a warm toffee glaze, served with ice cream. Classic Chinese dessert — caramelised, indulgent.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Banana Fritters With Ice Cream</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="650">650</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Crisp battered banana served with ice cream. Hot meets cold — a crowd favourite for good reason.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Pineapple Cinnamon Fritters With Ice Cream</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="650">650</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Pineapple rings in a cinnamon batter, fried until golden, served with ice cream. Tropical, spiced, and bright.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Milkshake</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="500">500</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Vanilla, strawberry or chocolate. Thick, cold, and made in-house. The Parklands finish.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Slice of Cake</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Ask the team for this week's flavour. Subject to availability.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Cake On Order</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="2000">2,000</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">½kg from KES 2,000 · 1kg from KES 3,000. Order ahead — speak to the team for flavour and timing.</span>
</li>
    </ul>
  </details>
  <details class="menu-accordion" name="menu-groups" id="hot-beverages" itemscope itemtype="https://schema.org/MenuSection">
    <summary class="accordion-trigger">
      <span class="accordion-title" itemprop="name">Hot Beverages</span>
      <span class="accordion-badge">12 Dishes</span>
    </summary>
    <ul class="accordion-panel-list" role="list">
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Caffe Latte</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Espresso with steamed milk. The everyday benchmark — smooth, warm, and reliable.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Cappuccino</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Equal parts espresso, steamed milk, and foam. The Italian morning classic — right at your table.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Chai Latte</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Spiced chai with steamed milk. Warming, aromatic, and the right companion to any dessert.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Espresso</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">A single concentrated shot. No dilution, no ceremony — just pure coffee.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Latte Macchiato</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Steamed milk marked with espresso — layered, gentle, and visually elegant.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Mocha</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Espresso with chocolate and steamed milk. Coffee and cocoa — the indulgent middle ground.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Hot Chocolate</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Rich steamed chocolate milk. No coffee, all comfort — ideal for the table's non-coffee drinker.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Hot Water With Lemon &amp; Honey</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Fresh lemon and honey in hot water. Simple, restorative, and underrated.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Chinese Tea Pot</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="400">400</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">A pot of Chinese green or jasmine tea — the natural companion to the full Mister Wok experience.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Masala Tea Pot</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="400">400</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Spiced masala chai brewed in a pot. Bold, warming, and a Parklands afternoon staple.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Kenya Coffee Pot</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="400">400</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Kenyan filter coffee brewed in a pot. Single origin, full flavour, served black or with milk.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Kenya Tea Pot</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="400">400</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Classic Kenyan black tea brewed in a pot. Straightforward, strong, and always reliable.</span>
</li>
    </ul>
  </details>
  <details class="menu-accordion" name="menu-groups" id="beverages" itemscope itemtype="https://schema.org/MenuSection">
    <summary class="accordion-trigger">
      <span class="accordion-title" itemprop="name">Beverages</span>
      <span class="accordion-badge">23 Dishes</span>
    </summary>
    <ul class="accordion-panel-list" role="list">
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Sodas</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="200">200</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Coke, Sprite, Fanta — ask the team for today's selection.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Coke Lite</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="200">200</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Zero sugar. Full taste. The clean refresh.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Mineral Water – Small</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="150">150</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">500ml still water.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Mineral Water – Large</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="200">200</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">750ml still water.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Sparkling Water – Large</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="250">250</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Large sparkling water. The pairing choice for dim sum and seafood.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Fresh Juice</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Lime &amp; Ginger, Mango, Passion, Pineapple &amp; Mint, or Tree Tomato — pressed to order.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Fruit Cocktail Juice</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="400">400</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Mango, Passion or Tree Tomato — blended to order.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Mocktails</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="600">600</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Quiet Sunday, Shirley Temple, or Sprinter. Ask the bar team for the full list.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Kenyan Beer</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="450">450</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Tusker, White Cap or Pilsner — ask the team for today's availability.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Imported Beer</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="600">600</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Ask the bar team for today's imported selection.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Smirnoff Ice Black</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="450">450</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Chilled and ready. The table refresher for those who prefer it light.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">House Wine Per Glass</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="550">550</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Red or white — ask the team for today's pour.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Spirits — Gin / Vodka</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Bombay Sapphire, Gordons, Gilbeys, Absolute Vodka or Smirnoff — served as preferred.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Spirits — Rum</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="350">350</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Bacardi, Captain Morgan, Malibu Coconut or Myers.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Whisky</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="450">450</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Famous Grouse, Jameson or Johnnie Walker Red Label.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Johnnie Walker Black Label</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="550">550</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">The gold standard blended Scotch. Served neat, on the rocks, or with water.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Jack Daniels</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="550">550</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Tennessee whiskey. Served as preferred.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Chivas Regal 12 Years</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="600">600</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Blended Scotch, aged 12 years. Smooth, honeyed, and a fitting end to the Parklands experience.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Glenfiddich Special Reserve</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="600">600</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Single malt Scotch. The connoisseur's pour at Parklands.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Cognac / Brandy</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="700">700</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Courvoisier, Hennessy or Martel — the post-dinner pour.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Liqueur</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="400">400</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Amarula, Baileys, Cointreau, Drambuie, Kahlua or Tia Maria.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Cocktails</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="1000">1,000</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Dawa, Margarita, Mojito, Piñacolada, Restriction, Screw Driver, Tequila Sunrise — or ask the barman for anything not listed.</span>
</li>
    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">
  <div class="item-lead-wrapper">
    <span class="item-dish-name" itemprop="name">Wine By Bottle</span>
    <span class="item-leader-dots" aria-hidden="true"></span>
    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
      <meta itemprop="priceCurrency" content="KES">
      <span class="item-price-currency" aria-hidden="true">KES</span>
      <span class="price-amount" itemprop="price" content="2300">2,300</span>
    </div>
  </div>
  <span class="item-mini-meta" itemprop="description">Image Dry (Red/White) KES 2,400 · St. Mary's Sweet White KES 2,400 · For You Rosé KES 2,300 · Dompo Fortified KES 2,700 · Altar Sweet Fortified KES 2,700 · Rooster Unicorn Dry KES 2,800. Ask the team to see the full wine list.</span>
</li>
    </ul>
  </details>
'''

PHOTO_ENTRIES = '''


  /* ── NEW PARKLANDS-ONLY ITEMS ── */
  "Crab Meat and Sweet Corn Soup":            "soups.webp",
  "Fish Coriander Soup":                      "soups.webp",
  "Seafood Soup":                             "soups.webp",
  "Tom Yum Hed – Mushroom":                   "tom-yum-prawn.webp",
  "Tom Kha Hed – Mushroom":                   "tom-yum-prawn.webp",
  "Tom Kha Gai – Chicken":                    "tom-yum-prawn.webp",
  "Tom Kha Goong – Prawns":                   "tom-yum-prawn.webp",
  "Butterfly Salt & Pepper Prawns":           "golden-fried-prawns.webp",
  "Chilli Calamari":                          "chilli-fish.webp",
  "Seafood Tempura":                          "golden-fried-prawns.webp",
  "Sweet Chilli Lamb Special":                "lamb-ribs.webp",
  "Chicken Satay Skewers In Peanut Sauce":    "honey-chilli-chicken.webp",
  "Tofu Satay Skewers":                       "sesame-tofu-bites.webp",
  "Honey Chilli Tofu":                        "sesame-tofu-bites.webp",
  "Black Pepper Tofu":                        "sesame-tofu-bites.webp",
  "Mister Wok Golden 5 Special":              "shanghai-veg-tofu-mushroom-brocolli.webp",
  "Vegetable Tempura":                        "shan-tung-potato-wedges.webp",
  "Coconut Fish Special":                     "fish-in-garlic.webp",
  "Mandarin Steamed Whole Fish":              "fish-in-garlic.webp",
  "Steamed Fish Fillet":                      "fish-in-garlic.webp",
  "Ginger Crab":                              "ginger-crab.webp",
  "Crab in Garlic":                           "ginger-crab.webp",
  "Crab In Black Bean":                       "ginger-crab.webp",
  "Ginger Lobster":                           "ginger-crab.webp",
  "Lobster in Garlic":                        "ginger-crab.webp",
  "Lobster In Black Bean":                    "ginger-crab.webp",
  "Mushroom FuYong":                          "shanghai-veg-tofu-mushroom-brocolli.webp",
  "Chicken FuYong":                           "honey-chilli-chicken.webp",
  "Chicken and Mushroom FuYong":              "honey-chilli-chicken.webp",
  "Beef and Mushroom FuYong":                 "beef-mushroom.webp",
  "Prawn and Mushroom FuYong":                "golden-fried-prawns.webp",
'''

APPEND = {
    "soups": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Vegetable Man Chow Soup</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="450">450</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">A thick, starchy Manchurian-style vegetable soup with a bold, peppery finish. Deeply warming.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Vegetable Man Chow Soup from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Crab Meat and Sweet Corn Soup</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="800">800</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Delicate crab meat folded into a creamy sweet corn broth. A Parklands signature soup — rich, subtle, and worth the price.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Crab Meat and Sweet Corn Soup from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Fish Coriander Soup</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="700">700</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Tilapia in a fragrant coriander broth. Light, herbal, and clean — an ideal palate opener.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Fish Coriander Soup from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Seafood Soup</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="800">800</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">A market catch of prawn, fish and calamari in a seasoned Chinese stock. The ocean in a bowl.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Seafood Soup from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Tom Yum Hed – Mushroom</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="600">600</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Mushrooms simmered in a lemongrass, chilli and lime broth. The vegetarian Tom Yum — equally bold, no compromise.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Tom Yum Hed – Mushroom from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Tom Kha Hed – Mushroom</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="700">700</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Mushrooms simmered in coconut cream with chilli and lime. Silky, aromatic, and restorative.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Tom Kha Hed – Mushroom from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Tom Kha Gai – Chicken</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="700">700</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Chicken in a coconut cream broth with chilli and lime. Milder than Tom Yum, richer in texture.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Tom Kha Gai – Chicken from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Tom Kha Goong – Prawns</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="800">800</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Queen prawns in coconut cream with lemongrass, chilli and lime. The premium Tom Kha — ocean meets tropics.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Tom Kha Goong – Prawns from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
    "seafood-apps": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Prawn Crackers</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="400">400</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Light, airy prawn crackers — the classic table starter. Crisp on arrival.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Prawn Crackers from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Butterfly Salt &amp; Pepper Prawns</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1400">1,400</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Butterflied prawns tossed in salt, pepper and aromatic dry spices. Crisp shell, tender interior.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Butterfly Salt &amp; Pepper Prawns from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Chilli Calamari</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1500">1,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Squid florets tossed with bell peppers in a chilli-forward wok sauce. High heat, bold flavour.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Chilli Calamari from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Seafood Tempura</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1500">1,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Prawn, calamari and tilapia in a light Japanese-style tempura batter. Delicate crunch, fresh ocean flavour.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Seafood Tempura from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
    "chicken-apps": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Salt &amp; Pepper Chicken Wings Dry</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1100">1,100</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Chicken wings tossed dry in a salt and pepper crust. No sauce, no glaze — just clean spice and crunch.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Salt &amp; Pepper Chicken Wings Dry from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Chicken Satay Skewers In Peanut Sauce</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1200">1,200</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Marinated chicken on skewers, grilled and served with a rich house peanut sauce. A Southeast Asian classic.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Chicken Satay Skewers In Peanut Sauce from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
    "lamb-starters": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Sweet Chilli Lamb Special</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1200">1,200</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Tender lamb in a house sweet chilli glaze. The heat is present but restrained — balanced, sticky, and satisfying.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Sweet Chilli Lamb Special from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
    "veg-apps": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Special Bean Sprout Spring Rolls</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="600">600</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">4 pieces. Filled with fresh, crunchy mung bean sprouts — lighter than the standard roll, with satisfying snap in every bite.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Special Bean Sprout Spring Rolls from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Black Pepper Tofu</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="950">950</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Crisp tofu tossed in a bold black pepper sauce. Sharp, aromatic, and deeply savoury.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Black Pepper Tofu from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Tofu Satay Skewers</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="950">950</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Tofu cubes on skewers, served in the house Mister Wok sauce. Firm, flavourful, and unapologetically plant-based.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Tofu Satay Skewers from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Honey Chilli Tofu</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="950">950</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Crispy tofu glazed in honey and chilli. Sweet heat — the vegetarian crowd-pleaser on the Parklands menu.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Honey Chilli Tofu from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Schezuan Style Baby Corn</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="950">950</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Baby corn tossed in a Schezuan chilli sauce. Snappy, numbing, and addictive.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Schezuan Style Baby Corn from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Golden Fried Babycorn</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="950">950</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Baby corn deep-fried to a golden finish. Light batter, clean snap — a simple pleasure done right.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Golden Fried Babycorn from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Vegetable Tempura</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1000">1,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Garden vegetables nestled in a light, lacy tempura batter. Delicate and crisp — Japanese technique, wok sensibility.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Vegetable Tempura from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Vegetable Satay Skewers In Peanut Sauce</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1000">1,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Mixed vegetable skewers served with a rich house peanut sauce. Substantial, plant-forward, and fully satisfying.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Vegetable Satay Skewers In Peanut Sauce from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Mister Wok Golden 5 Special</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1000">1,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Babycorn, broccoli, carrots, mushroom and tofu — the house vegetable five. Wok-tossed at high heat, served as nature intended.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Mister Wok Golden 5 Special from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
    "dim-sum": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Har-Gow Prawn Dumplings</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1000">1,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">4 pieces. Classic dim sum — translucent steamed prawn dumplings. The benchmark of a dim sum kitchen. Allow 20 minutes.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Har-Gow Prawn Dumplings from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Chicken Shumai</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="800">800</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">4 pieces. Open-top wontons filled with minced chicken — a Cantonese staple. Steamed to order. Allow 20 minutes.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Chicken Shumai from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Prawn Shumai</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1000">1,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">4 pieces. Open-top wontons filled with whole prawn. The premium Shumai — clean, plump, and elegant. Allow 20 minutes.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Prawn Shumai from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
    "seafood-main": '    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Coconut Fish Special</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1400">1,400</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Foil-wrapped steamed tilapia bites in a rich coconut gravy. Gentle heat, tropical depth — the most requested seafood special at Parklands.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Coconut Fish Special from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Mandarin Steamed Whole Fish</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1500">1,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">A whole tilapia steamed with ginger and spring onion in soy. The Cantonese classic — purity of technique, depth of flavour.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Mandarin Steamed Whole Fish from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Steamed Fish Fillet</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1500">1,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Tilapia fillet steamed with ginger and spring onion in soy. Boneless, clean, and refined.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Steamed Fish Fillet from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Tilapia Fish Sizzler</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1500">1,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Tilapia on a cast-iron sizzler plate — sauce applied tableside. Theatrics with substance.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Tilapia Fish Sizzler from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Deep Fried Whole Fish</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1500">1,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">A whole tilapia fried until crackling crisp, finished with the chef\'s special sauce. Bold presentation, bold flavour.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Deep Fried Whole Fish from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Prawns In Black Bean Sauce</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1600">1,600</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Queen prawns wok-tossed in a bold fermented black bean sauce. Savoury depth, briny complexity.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Prawns In Black Bean Sauce from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Prawns In Soya Sauce</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1600">1,600</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Queen prawns in a light soya glaze. Clean, umami-forward, and delicate enough to let the prawn speak.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Prawns In Soya Sauce from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Schezuan Prawns</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1600">1,600</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Queen prawns in a Schezuan chilli oil base. Heat-forward, numbing on the edges, and powerfully aromatic.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Schezuan Prawns from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Thai Prawn Green Curry</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1700">1,700</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Queen prawns in a fragrant Thai green curry — coconut-based, herbaceous, with a clean chilli lift.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Thai Prawn Green Curry from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Thai Prawn Red Curry</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="1700">1,700</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Queen prawns in a rich Thai red curry — deeper, warmer, and more complex than the green. Served with steamed rice.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Thai Prawn Red Curry from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Ginger Crab</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="2000">2,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Whole crab — request on or off the shell — wok-tossed in a bold ginger sauce. A Parklands exclusive. Available subject to market supply.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Ginger Crab from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Crab in Garlic</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="2000">2,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Crab wok-tossed in fragrant garlic sauce. Clean, aromatic, and generous. Parklands only.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Crab in Garlic from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Crab In Black Bean</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="2000">2,000</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Crab in a fermented black bean sauce. Bold, umami-heavy, and unapologetically complex. Parklands only.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Crab In Black Bean from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Ginger Lobster</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="3500">3,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Lobster wok-tossed in a ginger sauce. The premium centrepiece — available subject to market supply. Parklands only.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Ginger Lobster from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Lobster in Garlic</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="3500">3,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Lobster in fragrant garlic sauce. The cleanest expression of a luxury protein — subject to market supply. Parklands only.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Lobster in Garlic from Mister Wok Parklands">Order</button>\n  </div>\n</li>    <li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">\n  <div class="item-lead-wrapper">\n    <span class="item-dish-name" itemprop="name">Lobster In Black Bean</span>\n    <span class="item-leader-dots" aria-hidden="true"></span>\n    <div class="item-price-box" itemprop="offers" itemscope itemtype="https://schema.org/Offer">\n      <meta itemprop="priceCurrency" content="KES">\n      <span class="item-price-currency" aria-hidden="true">KES</span>\n      <span class="price-amount" itemprop="price" content="3500">3,500</span>\n    </div>\n  </div>\n  <span class="item-mini-meta" itemprop="description">Lobster in fermented black bean sauce. Intense, deeply savoury, and completely memorable. Parklands only.</span>\n  <div class="item-order-row">\n    <button type="button" class="menu-item-order order-trigger" data-order-btn="true" aria-label="Order Lobster In Black Bean from Mister Wok Parklands">Order</button>\n  </div>\n</li>',
}

SECTION_CLOSE = re.compile(
    r'(?P<head><details class="menu-accordion" name="menu-groups" id="(?P<sid>[^"]+)"[^>]*>.*?)'
    r'(?P<close>    </ul>\r?\n  </details>)',
    re.DOTALL,
)

SOUP_BEVERAGE_NAMES = [
    "Sodas", "Coke Lite", "Coke Light", "Mineral Water – Small", "Mineral Water – Large",
    "Sparkling Water – Large", "Fresh Juice", "Fruit Cocktail Juice",
]

CHICKEN_WRAP_DESC = (
    "Wok-seared minced chicken with sweetcorn, wrapped in a fresh lettuce leaf. "
    "Light, clean, and assembled to order."
)

JUMP_NAV_PILLS = """
    <a href="#fuyong"        class="mjn-link mjn-solo"><span class="mjn-course">FuYong</span></a>
    <a href="#desserts"      class="mjn-link mjn-solo"><span class="mjn-course">Desserts</span></a>
    <a href="#hot-beverages" class="mjn-link mjn-solo"><span class="mjn-course">Hot Beverages</span></a>
    <a href="#beverages"     class="mjn-link mjn-solo"><span class="mjn-course">Beverages</span></a>"""

JSONLD_SECTIONS = """
    {
      \"@type\": \"MenuSection\",
      \"name\": \"FuYong\"
    },
    {
      \"@type\": \"MenuSection\",
      \"name\": \"Desserts\"
    },
    {
      \"@type\": \"MenuSection\",
      \"name\": \"Hot Beverages\"
    },
    {
      \"@type\": \"MenuSection\",
      \"name\": \"Beverages\"
    }"""

MODIFIED_SECTIONS = [
    "soups", "seafood-apps", "chicken-apps", "lamb-starters", "veg-apps",
    "dim-sum", "seafood-main", "wraps", "fuyong", "desserts", "hot-beverages", "beverages",
]


def all_section_ids(html: str) -> list[str]:
    return re.findall(r'name="menu-groups" id="([^"]+)"', html)

SECTION_MARKERS = {
    "soups": "Vegetable Man Chow Soup",
    "seafood-apps": "Prawn Crackers",
    "chicken-apps": "Salt &amp; Pepper Chicken Wings Dry",
    "lamb-starters": "Sweet Chilli Lamb Special",
    "veg-apps": "Special Bean Sprout Spring Rolls",
    "dim-sum": "Har-Gow Prawn Dumplings",
    "seafood-main": "Coconut Fish Special",
}
NEW_SECTION_MARKER = 'id="fuyong"'
PHOTO_MARKER = '"Crab Meat and Sweet Corn Soup"'


def repair_corruption(html: str) -> str:
    """Fix botched append where section id replaced closing tags."""
    for sid in ("soups", "veg-apps", "lamb-starters", "seafood-apps", "seafood-main"):
        html = html.replace(
            f"</li>{sid}\n  <details",
            "</li>\n    </ul>\n  </details>\n  <details",
        )
    return html


def extract_section(html: str, section_id: str) -> str | None:
    for m in SECTION_CLOSE.finditer(html):
        if m.group("sid") == section_id:
            return m.group(0)
    return None


def count_items_in_section(section_html: str) -> int:
    return len(re.findall(r'class="item-dish-name"', section_html))


def append_to_section(html: str, section_id: str, block: str) -> str:
    def repl(m):
        if m.group("sid") != section_id:
            return m.group(0)
        return m.group("head") + block + m.group("close")

    return SECTION_CLOSE.sub(repl, html, count=0)


def update_section_badge(html: str, section_id: str) -> str:
    section = extract_section(html, section_id)
    if not section:
        return html
    count = count_items_in_section(section)
    label = "Dish" if count == 1 else "Dishes"
    new_section = re.sub(
        r'<span class="accordion-badge">[^<]*</span>',
        f'<span class="accordion-badge">{count} {label}</span>',
        section,
        count=1,
    )
    return html.replace(section, new_section, 1)


def remove_soup_beverages(html: str) -> tuple[str, int]:
    section = extract_section(html, "soups")
    if not section:
        return html, 0
    removed = 0
    new_section = section
    for name in SOUP_BEVERAGE_NAMES:
        pat = (
            rf'    <li class="menu-item-row"[^>]*>.*?'
            rf'<span class="item-dish-name" itemprop="name">{re.escape(name)}</span>.*?</li>\n?'
        )
        new_section, n = re.subn(pat, "", new_section, count=1, flags=re.DOTALL)
        removed += n
    if removed:
        html = html.replace(section, new_section, 1)
    return html, removed


def update_chicken_wrap(html: str) -> str:
    section = extract_section(html, "wraps")
    if not section:
        return html
    new_section = re.sub(
        r'(<span class="item-dish-name" itemprop="name">Chicken Wrap</span>.*?'
        r'<span class="price-amount" itemprop="price" content=")\d+(">)[^<]*(</span>)',
        r"\g<1>1000\g<2>1,000\g<3>",
        section,
        count=1,
        flags=re.DOTALL,
    )
    new_section = re.sub(
        r'(<span class="item-dish-name" itemprop="name">Chicken Wrap</span>.*?'
        r'<span class="item-mini-meta" itemprop="description">)[^<]*(</span>)',
        rf"\g<1>{CHICKEN_WRAP_DESC}\g<2>",
        new_section,
        count=1,
        flags=re.DOTALL,
    )
    return html.replace(section, new_section, 1)


def insert_new_sections(html: str) -> str:
    if NEW_SECTION_MARKER in html:
        return html
    return html.replace("</main>", NEW_SECTIONS + "\n</main>", 1)


def insert_jump_nav(html: str) -> str:
    if 'href="#fuyong"' in html:
        return html
    anchor = '<a href="#kiddie"       class="mjn-link mjn-solo"><span class="mjn-course">Kiddie</span></a>'
    return html.replace(anchor, anchor + JUMP_NAV_PILLS, 1)


def insert_jsonld(html: str) -> str:
    if '"name": "FuYong"' in html:
        return html
    return html.replace(
        '    {\n      "@type": "MenuSection",\n      "name": "Kiddie Menu"\n    }\n  ]',
        '    {\n      "@type": "MenuSection",\n      "name": "Kiddie Menu"\n    },' + JSONLD_SECTIONS + "\n  ]",
        1,
    )


def update_meta_counts(html: str, dishes: int, categories: int) -> str:
    html = re.sub(
        r"(<title>Mister Wok Parklands Full Menu 2026 \| )\d+( [Dd]ishes)",
        rf"\g<1>{dishes} Dishes",
        html,
        count=1,
    )
    html = re.sub(
        r'content="Full Mister Wok Parklands menu 2026\. \d+ dishes across \d+ categories',
        f'content="Full Mister Wok Parklands menu 2026. {dishes} dishes across {categories} categories',
        html,
        count=1,
    )
    html = re.sub(
        r'(meta property="og:description" content=")\d+ dishes',
        rf"\g<1>{dishes} dishes",
        html,
        count=1,
    )
    html = re.sub(
        r"(<p class=\"menu-page-sub\">)\d+ dishes · \d+ categories",
        rf"\g<1>{dishes} dishes · {categories} categories",
        html,
        count=1,
    )
    html = re.sub(
        r"(The Parklands full menu has )\d+ dishes across \d+ categories",
        rf"\g<1>{dishes} dishes across {categories} categories",
        html,
        count=1,
    )
    html = re.sub(
        r"(Full menu · )\d+ dishes",
        rf"\g<1>{dishes} dishes",
        html,
        count=1,
    )
    html = re.sub(
        r"22229 dishes",
        f"{dishes} dishes",
        html,
    )
    return html


def patch_photos(text: str) -> str:
    if PHOTO_MARKER in text:
        return text
    return text.replace("\n};", "\n" + PHOTO_ENTRIES + "\n};", 1)


def count_categories(html: str) -> int:
    return len(re.findall(r'name="menu-groups" id="[^"]+"', html))


def count_dishes(html: str) -> int:
    return len(re.findall(r'class="item-dish-name"', html))


def validate(html: str, photos: str) -> dict:
    results = {}

    soups = extract_section(html, "soups") or ""
    new_soup_names = [
        "Vegetable Man Chow Soup", "Crab Meat and Sweet Corn Soup", "Fish Coriander Soup",
        "Seafood Soup", "Tom Yum Hed – Mushroom", "Tom Kha Hed – Mushroom",
        "Tom Kha Gai – Chicken", "Tom Kha Goong – Prawns",
    ]
    results[1] = all(n in soups for n in new_soup_names)
    results[2] = not any(n in soups for n in SOUP_BEVERAGE_NAMES)

    sa = extract_section(html, "seafood-apps") or ""
    results[3] = all(n in sa for n in [
        "Prawn Crackers", "Butterfly Salt &amp; Pepper Prawns", "Chilli Calamari", "Seafood Tempura",
    ])

    ca = extract_section(html, "chicken-apps") or ""
    results[4] = all(n in ca for n in [
        "Salt &amp; Pepper Chicken Wings Dry", "Chicken Satay Skewers In Peanut Sauce",
    ])

    la = extract_section(html, "lamb-starters") or ""
    results[5] = "Sweet Chilli Lamb Special" in la

    va = extract_section(html, "veg-apps") or ""
    veg_new = [
        "Special Bean Sprout Spring Rolls", "Black Pepper Tofu", "Tofu Satay Skewers",
        "Honey Chilli Tofu", "Schezuan Style Baby Corn", "Golden Fried Babycorn",
        "Vegetable Tempura", "Vegetable Satay Skewers In Peanut Sauce", "Mister Wok Golden 5 Special",
    ]
    results[6] = all(n in va for n in veg_new)

    wraps = extract_section(html, "wraps") or ""
    results[7] = (
        "Chicken Wrap" in wraps
        and 'content="1000">1,000' in wraps
        and CHICKEN_WRAP_DESC in wraps
    )

    ds = extract_section(html, "dim-sum") or ""
    results[8] = all(n in ds for n in ["Har-Gow Prawn Dumplings", "Chicken Shumai", "Prawn Shumai"])

    sm = extract_section(html, "seafood-main") or ""
    seafood_new = [
        "Coconut Fish Special", "Mandarin Steamed Whole Fish", "Steamed Fish Fillet",
        "Tilapia Fish Sizzler", "Deep Fried Whole Fish", "Prawns In Black Bean Sauce",
        "Prawns In Soya Sauce", "Schezuan Prawns", "Thai Prawn Green Curry", "Thai Prawn Red Curry",
        "Ginger Crab", "Crab in Garlic", "Crab In Black Bean", "Ginger Lobster",
        "Lobster in Garlic", "Lobster In Black Bean",
    ]
    results[9] = all(n in sm for n in seafood_new)

    for num, sid, expected in [
        (10, "fuyong", 5), (11, "desserts", 8), (12, "hot-beverages", 12), (13, "beverages", 23),
    ]:
        sec = extract_section(html, sid) or ""
        results[num] = (
            f'id="{sid}"' in html
            and 'name="menu-groups"' in sec
            and count_items_in_section(sec) == expected
        )

    results[14] = all(x in html for x in [
        'href="#fuyong"', 'href="#desserts"', 'href="#hot-beverages"', 'href="#beverages"',
    ])
    results[15] = all(x in html for x in [
        '"name": "FuYong"', '"name": "Desserts"', '"name": "Hot Beverages"', '"name": "Beverages"',
    ])

    dishes = count_dishes(html)
    categories = count_categories(html)
    results[16] = (
        f"{dishes} dishes" in html.lower()
        and f"{categories} categories" in html
        and "138 dishes" not in html.lower()
        and "22229 dishes" not in html
    )

    photo_keys = re.findall(r'"([^"]+)":\s*"[^"]+\.webp"', PHOTO_ENTRIES)
    results[17] = all(k in photos for k in photo_keys) and len(photo_keys) == 31

    li_pattern = re.compile(
        r'<li class="menu-item-row" role="listitem" itemscope itemtype="https://schema.org/MenuItem">'
        r'.*?<span class="item-dish-name" itemprop="name">',
        re.DOTALL,
    )
    all_lis = re.findall(r'<li class="menu-item-row"[^>]*>.*?</li>', html, re.DOTALL)
    results[18] = all(li_pattern.match(li) for li in all_lis)

    new_details = re.findall(
        r'<details class="menu-accordion" name="menu-groups" id="(fuyong|desserts|hot-beverages|beverages)"',
        html,
    )
    results[19] = len(new_details) == 4

    badge_ok = True
    for sid in all_section_ids(html):
        sec = extract_section(html, sid)
        if not sec:
            badge_ok = False
            break
        count = count_items_in_section(sec)
        m = re.search(r'<span class="accordion-badge">(\d+) Dishes</span>', sec)
        if not m or int(m.group(1)) != count:
            badge_ok = False
            break
    results[20] = badge_ok

    return results, dishes, categories


def main():
    html = MENU.read_text(encoding="utf-8")
    photos = PHOTOS.read_text(encoding="utf-8")

    html = repair_corruption(html)
    html = html.replace("22229 dishes", "229 dishes")

    for sid, block in APPEND.items():
        marker = SECTION_MARKERS[sid]
        section = extract_section(html, sid) or ""
        if marker not in section:
            html = append_to_section(html, sid, block)

    html, removed = remove_soup_beverages(html)
    html = update_chicken_wrap(html)
    html = insert_new_sections(html)
    html = insert_jump_nav(html)
    html = insert_jsonld(html)

    for sid in all_section_ids(html):
        html = update_section_badge(html, sid)

    dishes = count_dishes(html)
    categories = count_categories(html)
    html = update_meta_counts(html, dishes, categories)

    for sid in all_section_ids(html):
        html = update_section_badge(html, sid)

    MENU.write_text(html, encoding="utf-8")

    photos = patch_photos(photos)
    PHOTOS.write_text(photos, encoding="utf-8")

    html = MENU.read_text(encoding="utf-8")
    photos = PHOTOS.read_text(encoding="utf-8")
    results, dishes, categories = validate(html, photos)

    print("PHASE 1B PARKLANDS MENU PATCH — COMPLETE")
    print("=" * 52)
    print(f"Dish count:     {dishes}")
    print(f"Category count: {categories}")
    if removed:
        print(f"Removed {removed} misplaced beverage item(s) from Soups")
    else:
        print("No beverages removed from Soups (none found)")
    print("=" * 52)
    labels = {
        1: "Soups: 8 new items added",
        2: "Soups: beverage items removed",
        3: "Seafood Appetizers: 4 new items",
        4: "Chicken Appetizers: 2 new items",
        5: "Lamb Appetizers: Sweet Chilli Lamb",
        6: "Vegetarian Appetizers: 9 new items",
        7: "Wraps: Chicken Wrap price/description updated",
        8: "Dim Sum: Har-Gow + 2 Shumai",
        9: "Seafood Main: 15 new items",
        10: "FuYong section (5 items)",
        11: "Desserts section (8 items)",
        12: "Hot Beverages section (12 items)",
        13: "Beverages section (23 items)",
        14: "Jump nav: 4 new pills",
        15: "JSON-LD: 4 new MenuSection entries",
        16: "Title/meta counts updated",
        17: "menu-photos.js: 31 new entries",
        18: "All items match canonical pattern",
        19: "New details carry name=menu-groups",
        20: "accordion-badge counts correct",
    }
    passed = sum(1 for k, v in results.items() if v)
    for i in range(1, 21):
        status = "PASS" if results.get(i) else "FAIL"
        print(f"[{status}] #{i:02d} {labels[i]}")
    print("=" * 52)
    print(f"SCORE: {passed}/20")
    if passed < 20:
        failed = [i for i, v in results.items() if not v]
        print(f"Failed checks: {failed}")


if __name__ == "__main__":
    main()
