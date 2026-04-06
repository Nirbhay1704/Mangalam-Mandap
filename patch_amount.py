import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the amount cells
content = content.replace('<td class="col-amount amount-display">0</td>', '<td class="col-amount amount-display editable" contenteditable="true">0</td>')

# 2. Update bindInputs
old_bind_pattern = re.compile(r'function bindInputs\(row\) \{[\s\S]*?\n        \}')
new_bind = r"""function bindInputs(row) {
            const calcInputs = row.querySelectorAll('.l-input, .w-input, .h-input, .qty-input, .days-input, .rate-input');
            const amountDisplay = row.querySelector('.amount-display');
            
            calcInputs.forEach(input => {
                input.addEventListener('input', () => {
                    if(amountDisplay) amountDisplay.dataset.manual = "false";
                    calculateTotals();
                });
            });

            if (amountDisplay) {
                amountDisplay.addEventListener('input', () => {
                    amountDisplay.dataset.manual = "true";
                    calculateTotals();
                });
                amountDisplay.addEventListener('blur', () => {
                    if(amountDisplay.dataset.manual === "true") {
                        let val = parseFloat(amountDisplay.innerText.replace(/[^\d.-]/g, '')) || 0;
                        amountDisplay.innerText = formatNumber(val);
                    }
                });
            }
        }"""
content = old_bind_pattern.sub(lambda m: new_bind, content, count=1)


# 3. Update calculateTotals
old_calc_pattern = re.compile(r'let amount = 0;\s*if \(l > 0 && w > 0\) \{[\s\S]*?grandTotal \+= amount;')
new_calc = r"""let amount = 0;
                    const isManual = amountDisplay.dataset.manual === "true";
                    
                    if (!isManual) {
                        if (l > 0 && w > 0) {
                            amount = l * w * rate * days;
                            if (qty > 0) amount *= qty; // Multiply qty if they also added pieces for multiple items of same L * W
                        } else if (qty > 0) {
                            amount = qty * rate * days;
                        } else if (rate > 0) {
                            amount = rate * days;
                        }
                        amountDisplay.innerText = formatNumber(amount);
                    } else {
                        amount = parseFloat(amountDisplay.innerText.replace(/[^\d.-]/g, '')) || 0;
                    }
                    grandTotal += amount;"""
content = old_calc_pattern.sub(lambda m: new_calc, content, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
