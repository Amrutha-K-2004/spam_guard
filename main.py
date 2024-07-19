# //FINAL PROJECT FOR PRESENTATION
import math
import tkinter as tk

# CALCULATE LOG PROB
def calculate_log_probabilities(word_counts, total_count):
    probabilities = [0.0] * 57
    for i in range(57):
        probabilities[i] = math.log(word_counts[i] / total_count) if word_counts[i] != 0 else float('-inf')
    return probabilities

# READ DATA FROM TRAINING.TXT AND PROCESS INTO A 2D ARRAY
dataset = []
with open("training.txt") as textFile:
    for line in textFile:
        rows = [float(item.strip()) for item in line.split(',')]
        dataset.append(rows)

# LAPLACE SMOOTHING OF 0.01 ADDED TO ALL VALUES 
for ele in dataset:
    for i in range(57):
        ele[i] += 0.01

# INITIALISE word_ham and word_spam ARRAY 
word_ham = [0.0] * 57
word_spam = [0.0] * 57

# FILL THE ARRAY -CONVERT 2D ARRAY INTO 1D ARRAY(S)
for data in dataset:
    if data[57] == 1.0:
        for j in range(57):
            word_spam[j] += data[j]
    else:
        for j in range(57):
            word_ham[j] += data[j]

# FIND SUM OF ALL ELEMENTS IN THE ARRAY
total_spam = sum(word_spam)
# DIVIDE  EACH ELEMENT BY SUM AND TAKE LOG
prob_spam = calculate_log_probabilities(word_spam, total_spam)

# CARRY ON SAME PROCEDURE FOR HAM EMAIL
total_ham = sum(word_ham)
prob_ham = calculate_log_probabilities(word_ham, total_ham)

# TKINTER GUI PART 
class SpamHamClassifier:
    def __init__(self, root):
        self.root = root
        self.root.title("Spam Guard ")
        self.root.state('zoomed')  # Fullscreen mode
        self.root.configure(bg='blue4')  # Change background color
        self.setup_main_page()

    def setup_main_page(self):
        # Clear the current page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display heading
        heading_label = tk.Label(self.root, text="SPAM-GUARD", font=('Arial', 40, 'bold'), bg='blue4', fg='green1')
        heading_label.pack(pady=10)

        # Display first image
        self.img1 = tk.PhotoImage(file="intro_pic.png")
        self.img1_label = tk.Label(self.root, image=self.img1, bg='blue4')
        self.img1_label.pack(pady=10)

        self.input_label = tk.Label(self.root, text="Enter email for classification:", font=('Comic Sans MS', 26,'bold'), bg='blue4', fg='green2')
        self.input_label.pack(pady=10)

        # Use Text widget instead of Entry widget
        self.input_text = tk.Text(self.root, width=80, height=5, font=('Arial', 20))
        self.input_text.pack(pady=10)

        # Animation for the input text field
        self.animate_entry(self.input_text)

        # Create a frame to hold buttons in the same line
        button_frame = tk.Frame(self.root, bg='blue4')
        button_frame.pack(pady=10)

        self.next_button = tk.Button(button_frame, text="Check", command=self.process_input, font=('Arial', 20), fg='black', bg='green1')
        self.next_button.pack(side='left', padx=10)

        # Animation for the "Check" button
        self.animate_button(self.next_button)

        # Display "About" button
        about_button = tk.Button(button_frame, text="About", command=self.show_about_page, font=('Arial', 20), fg='black', bg='green1')
        about_button.pack(side='left', padx=10)

        # Animation for the "About" button
        self.animate_button(about_button)

    def process_input(self):
        user_input = self.input_text.get("1.0", tk.END).strip()
        if user_input:
            array_57 = self.generate_57_valued_array(user_input)
            self.show_classification_page(array_57)

    def generate_57_valued_array(self, email_text):
        words_list = [
            "make", "address", "all", "3d", "our", "over", "remove", "internet", "order", "mail", "receive",
            "will", "people", "report", "addresses", "free", "business", "email", "you", "credit", "your",
            "font", "000", "money", "hp", "hpl", "george", "650", "lab", "labs", "telnet", "857", "data",
            "415", "85", "technology", "1999", "parts", "pm", "direct", "cs", "meeting", "original",
            "project", "re", "edu", "table", "conference", ";", "(", "[", "!", "$", "#"
        ]
        freq_dict = {word: 0 for word in words_list}
        words = email_text.lower().split()
        for word in words:
            if word in freq_dict:
                freq_dict[word] += 1

        total_words = len(words)
        freq_percentages = []
        
        for word in words_list:
            freq = freq_dict[word]
            freq_percentage = 100 * freq / total_words if total_words > 0 else 0
            freq_percentages.append(freq_percentage)
        
        additional_values = [5.1915, 52.173, 283.29]
        freq_percentages.extend(additional_values)

        return freq_percentages

    def show_classification_page(self, array_57):
        # Clear the current page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display classify button
        classify_button = tk.Button(self.root, text="Classify", command=lambda: self.classify_and_display_result(array_57), font=('Arial', 20), bg='green yellow')
        classify_button.pack(pady=20)

        # Display back button
        back_button = tk.Button(self.root, text="Back", command=self.setup_main_page, font=('Arial', 20), bg='green yellow')
        back_button.pack(pady=20)

        # Animation for the "Classify" button
        self.animate_button(classify_button)

    def classify_and_display_result(self, test_instance):
        log_rat = 0.0
        for j in range(57):
            log_rat += (prob_spam[j] - prob_ham[j]) * test_instance[j]
        
        result = "spam" if log_rat >= 0 else "ham"
        result_color = "firebrick1" if result == "spam" else "chartreuse2"

        # Clear the current page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display result text
        result_label = tk.Label(self.root, text=f"Result: {result}", font=('Arial', 50), bg='blue4', fg=result_color)
        result_label.pack(pady=20)

        # Display appropriate image
        if result == "spam":
            img = tk.PhotoImage(file="spam.png")
        else:
            img = tk.PhotoImage(file="ham.png").subsample(3)   

        img_label = tk.Label(self.root, image=img, bg='blue4')
        img_label.pack(pady=20)

        # Display back button
        back_button = tk.Button(self.root, text="Back", command=self.setup_main_page, font=('Arial', 20), bg='green1')
        back_button.pack(pady=20)

        # Keep a reference to the image to prevent garbage collection
        self.img_ref = img

        # Animation for the result image
        self.animate_image(img_label)

    def show_about_page(self):
        # Clear the current page
        for widget in self.root.winfo_children():
            widget.destroy()

        # Display "About" text (Lorem Ipsum)
        about_text = (
        "SPAM GUARD :\n\n"

"Welcome to our advanced Spam Checking App, a state-of-the-art solution designed to help you filter and manage your emails effectively. In today's digital age, spam emails are more prevalent than ever, making it essential to have a reliable tool to distinguish between spam and legitimate emails. We use  cutting-edge machine learning algorithms (Naive bayes )to provide accurate and efficient spam detection.\n"
"\nFOLLOWING ARE THE TEST RESULTS COMPUTED (FOR 200 EMAILS ) :\n\n" 
 "TRUE POSITIVE  : 82.0\n"
 "TRUE NEGATIVE  : 69.0\n"
 "FALSE NEGATIVE : 20.0\n"
 "FALSE POSITIVE : 29.0\n"
 "ACCURACY DERIVED FROM THIS CLASSIFIER IS : 75.52 %"

        )
        about_label = tk.Label(self.root, text=about_text, font=('Arial', 20), bg='blue4',fg='lawngreen', wraplength=1000, justify='left')
        about_label.pack(pady=20)

        # Display back button
        back_button = tk.Button(self.root, text="Back", command=self.setup_main_page, font=('Arial', 20), bg='green2')
        back_button.pack(pady=5)

    def animate_button(self, button):
        def on_enter(event):
            button.config(bg='green1')
        
        button.bind("<Enter>", on_enter)

    def animate_image(self, label):
        # Animation to pulse once
        def pulse(count=0):
            if count < 5:
                current_size = label.winfo_width()
                new_size = current_size + 30 if current_size < 300 else 200
                label.config(width=new_size, height=new_size)
                self.root.after(50, pulse, count + 1)
        
        pulse()

    def animate_entry(self, entry):
        def on_focus_in(event):
            entry.config(bg='floralwhite')
        
        def on_focus_out(event):
            entry.config(bg='red')
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

# Initialize Tkinter app
root = tk.Tk()
app = SpamHamClassifier(root)
root.mainloop()
# //END 