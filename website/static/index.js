const swiper = new Swiper(".swiper", {
  // Optional parameters
  direction: "vertical",
  loop: true,

  // If we need pagination
  pagination: {
    el: ".swiper-pagination",
  },

  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  // And if we need scrollbar
  scrollbar: {
    el: ".swiper-scrollbar",
  },
});

const translations = {
  en: {
    whatWeDo: "WHAT WE DO",
    neuralNetwork: "THE NEURAL NETWORKS",
    typesOfCulture: "TYPES OF CULTURE",
    aboutUs: "ABOUT US",
    maps: "MAPS",
    desc: "AgriBee is a platform that helps agricultural businesses significantly increase their profits and utilize land to harvest crops without depleting soil. AgriBee analyzes climate and soil type, predicts wildfires and landslides, advises what is best to plant in a given area, and with which other plants to alternate cultivation so as not to deplete soil resources. By integrating AI-driven insights, AgriBee empowers farmers to optimize yield while preserving the environment for future generations.",
    wildfires:
      "The neural network harnesses advanced deep learning techniques to analyze satellite images and accurately detect wildfires. Leveraging state-of-the-art convolutional layers and robust  optimization algorithms, it ensures precise identification even in challenging scenarios. Designed to support early intervention and disaster management, this model is a powerful tool for safeguarding our planet against wildfire risks.",
    landslides:
      "The neural network is a cutting-edge model designed to identify landslides using satellite imagery. Utilizing a sophisticated    U-Net architecture, it delivers highly accurate segmentation  results, pinpointing areas affected by landslides with exceptional precision. This powerful tool is invaluable for disaster response and planning, helping communities mitigate risks and enhance safety.",
    typesOfCultureDesc: "TYPES OF CULTURE",
    locationPlaceholder: "Enter a location",
    footer:
      "We harness the power of artificial intelligence to create innovative solutions for a connected and sustainable future. Contact us to find out how our technologies can transform your industry. Let's shape the future together. Contact us at: agribee.contact@gmail.com",
  },
  uk: {
    whatWeDo: "НАША ДІЯЛЬНІСТЬ",
    neuralNetwork: "НЕЙРОННІ МЕРЕЖІ",
    typesOfCulture: "ТИПИ КУЛЬТУР",
    aboutUs: "ПРО НАС",
    maps: "КАРТИ",
    desc: "AgriBee - це платформа, яка допомагає аграрному бізнесу значно збільшити свої прибутки та використовувати землю для збору врожаю без виснаження ґрунту. AgriBee аналізує клімат і тип ґрунту, прогнозує лісові пожежі та зсуви, радить, що найкраще садити на даній ділянці, і з якими іншими рослинами чергувати вирощування, щоб не виснажувати ґрунтові ресурси. Інтегруючи знання, отримані завдяки штучному інтелекту, AgriBee дає можливість фермерам оптимізувати врожайність, зберігаючи при цьому навколишнє середовище для майбутніх поколінь.",
    wildfires:
      "Нейромережа використовує передові методи глибокого навчання для аналізу супутникових знімків і точного виявлення лісових пожеж. Використовуючи найсучасніші згорткові шари та надійні алгоритми оптимізації, вона забезпечує точну ідентифікацію навіть у складних сценаріях. Розроблена для підтримки раннього втручання та управління катастрофами, ця модель є потужним інструментом для захисту нашої планети від ризиків лісових пожеж.",
    landslides:
      "Ця нейронна мережа - це найсучасніша модель, розроблена для виявлення зсувів за допомогою супутникових знімків. Використовуючи складну архітектуру U-Net, вона забезпечує високоточні результати сегментації, визначаючи зони, уражені зсувами, з винятковою точністю. Цей потужний інструмент є неоціненним для реагування на катастрофи й планування, допомагаючи громадам зменшити ризики та підвищити безпеку.",
    locationPlaceholder: "Введіть місце розташування",
    footer:
      "Ми використовуємо можливості штучного інтелекту, щоб створювати інноваційні рішення. Зв'яжіться з нами, щоб дізнатися, як наші технології можуть трансформувати вашу галузь. Нумо формувати майбутнє разом! Наші контакти: agribee.contact@gmail.com",
  },
};

function changeLanguage(language) {
  document.querySelector(".wwd_head").textContent =
    translations[language].whatWeDo;
  document.querySelector(".tnn_head").textContent =
    translations[language].neuralNetwork;
  document.querySelector(".toc_head").textContent =
    translations[language].typesOfCulture;
  document.querySelector(".wwd_text").textContent = translations[language].desc;
  document.querySelector(".tnn_text").textContent =
    translations[language].wildfires;
  document.querySelector(".wwd1_text").textContent =
    translations[language].landslides;
  document.querySelector(".about_us_footer").textContent =
    translations[language].aboutUs;
  document.querySelector(".about_us").textContent =
    translations[language].footer;

  document
    .querySelector(".search-input")
    .setAttribute("placeholder", translations[language].locationPlaceholder);

  const navLinks = document.querySelectorAll("nav a");
  navLinks[0].textContent = translations[language].whatWeDo;
  navLinks[1].textContent = translations[language].neuralNetwork;
  navLinks[2].textContent = translations[language].typesOfCulture;
  navLinks[3].textContent = translations[language].maps;
  navLinks[4].textContent = translations[language].aboutUs;
}

document.getElementById("language-btn").addEventListener("click", function () {
  document.getElementById("language-dropdown").classList.toggle("active");
});

const languageOptions = document.querySelectorAll(".language-option");
const currentFlag = document.getElementById("current-flag");

languageOptions.forEach((option) => {
  option.addEventListener("click", function () {
    const selectedLang = this.dataset.lang;
    if (selectedLang === "en") {
      currentFlag.src = "/static/images/usa.png";
    } else if (selectedLang === "uk") {
      currentFlag.src = "/static/images/ua.png";
    }

    document.getElementById("language-dropdown").classList.remove("active");

    changeLanguage(selectedLang);
  });
});
