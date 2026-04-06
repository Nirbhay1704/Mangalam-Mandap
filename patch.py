import codecs

items = [
    "ડોમ સભામંડપ", "ડોમ રસોડા માટે", "ડોમ બેક સાઇડ", "સ્ટેજ", "વ્યાસપીઠ સ્ટેજ",
    "વ્યાસપીઠ", "સ્ટેજ થીમ", "સ્ટેજ ફ્લોરીંગ", "અલગ સ્ટેજ", "રેલીંગ",
    "ડોમ ફોલરીંગ", "રસોડા ફોલરીંગ", "મંડપ ગાળા", "કાઉન્ટર પાટ", "કાઉન્ટર ટેબર મઢીને તૈયાર",
    "રાઉન્ડ ટેબલ", "સ્ટેજ દાદર", "સોફા સ્ટીલ", "સોફા લેઘર", "ખુરશી",
    "લગ્ન મંડપ", "એન્ટ્રી બેલ્ટ", "એન્ટી ગેટ", "ગેટ કમાન", "ગજીપો",
    "ગાદલાં", "તકિયાં", "ઓશીકા", "બ્લેન્કેટ", "રજાઇ",
    "સાઇડ પારટેશન", "V.I .P. રૂમ"
]

html_rows = ""
for i, item in enumerate(items):
    html_rows += f'''                <tr class="item-row">
                    <td class="col-sn"><input type="number" class="sn-input" value="{i+1}"></td>
                    <td class="col-particular editable" contenteditable="true">{item}</td>
                    <td class="col-unit">
                        <select class="unit-select">
                            <option value="ચો.ફુટ">ચો.ફુટ</option>
                            <option value="સેટ">સેટ</option>
                            <option value="નંગ">નંગ</option>
                            <option value="રનિંગ ફુટ">રનિંગ ફુટ</option>
                        </select>
                    </td>
                    <td class="col-width"><input type="number" class="w-input" value="" step="any"></td>
                    <td class="col-length"><input type="number" class="l-input" value="" step="any"></td>
                    <td class="col-height"><input type="number" class="h-input" value="" step="any"></td>
                    <td class="col-qty"><input type="number" class="qty-input" value="" step="any"></td>
                    <td class="col-days"><input type="number" class="days-input" value="" step="any" placeholder="1"></td>
                    <td class="col-rate"><input type="number" class="rate-input" value="" step="any"></td>
                    <td class="col-amount amount-display">0</td>
                </tr>\n'''

with codecs.open('index.html', 'r', 'utf-8') as f:
    content = f.read()

# Replace tbody
start_marker = '<tbody id="quotation-body">\n'
end_marker = '                <tr class="total-row" id="total-row">'
start_idx = content.find(start_marker) + len(start_marker)
end_idx = content.find(end_marker)

new_content = content[:start_idx] + html_rows + content[end_idx:]

# Remove the JS initialization
js_start = new_content.find('// Add event listeners to initial inputs')
js_end = new_content.find('calculateTotals();\\n        });')

# Fallback safely if exact matches miss
if js_end == -1:
    js_end = new_content.find('calculateTotals();\\r\\n        });')
if js_end == -1:
    js_end = new_content.find('calculateTotals();\\n        });')

split_marker = 'calculateTotals();\\n        });'
parts = new_content.split(split_marker)
if len(parts) > 1:
    content_after = parts[1]
    
    replacement_js = '''// Add event listeners to initial inputs
        document.addEventListener('DOMContentLoaded', () => {
            const rows = document.querySelectorAll('.item-row');
            rows.forEach(r => bindInputs(r));
            calculateTotals();
        });'''

    final_content = new_content[:js_start] + replacement_js + content_after

    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(final_content)
    print("Patch successful!")
else:
    print("Error finding JS markers")
