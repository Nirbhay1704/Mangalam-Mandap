import re
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

items_html = "\n"
for i, name in enumerate(items):
    items_html += f'''                <tr class="item-row">
                    <td class="col-sn"><input type="number" class="sn-input" value="{i+1}"></td>
                    <td class="col-particular editable" contenteditable="true">{name}</td>
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

try:
    with codecs.open('index.html', 'r', 'utf-8') as f:
        text = f.read()

    # 1. Replace Table Body
    start_tag = '<tbody id="quotation-body">'
    end_tag = '<tr class="total-row" id="total-row">'
    
    start_idx = text.find(start_tag) + len(start_tag)
    end_idx = text.find(end_tag)
    
    text = text[:start_idx] + items_html + "                " + text[end_idx:]

    # 2. Remove JS preloader
    pattern = r'// Add event listeners to initial inputs and load default list.*?calculateTotals\(\);\s*}\);'
    replacement = """// Add event listeners to initial inputs
        document.addEventListener('DOMContentLoaded', () => {
            const rows = document.querySelectorAll('.item-row');
            rows.forEach(r => bindInputs(r));
            calculateTotals();
        });"""
        
    text = re.sub(pattern, replacement, text, flags=re.DOTALL)

    with codecs.open('index.html', 'w', 'utf-8') as f:
        f.write(text)
        
    print("SUCCESS: Hardcoded HTML rows appended securely.")
except Exception as e:
    print(f"FAILED: {str(e)}")
