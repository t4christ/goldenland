let idVal = 0;
const housingData = [
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner2.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner2.jpeg' %}",
    price: 30000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner1.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner1.jpeg' %}",
    price: 40000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner3.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner3.jpeg' %}",
    price: 60000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner2.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner2.jpeg' %}",
    price: 45000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner4.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner4.jpeg' %}",
    price: 35000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner2.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner2.jpeg' %}",
    price: 55000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner2.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner2.jpeg' %}",
    price: 65000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
  {
    id: ++idVal,
    link: "./html/pageListing.html",
    linkTwo: "pageListing.html",
    image: "{% static 'assets/images/banner2.jpeg' %}",
    imageTwo: "{% static 'assets/images/banner2.jpeg' %}",
    price: 63000,
    location: "44B, Ejigbo, Lagos, Nigeria",
  },
];

const property = housingData.map(
  ({ id, link, linkTwo, image, imageTwo, price, location }) => {
    return `<div class="property_image animate_up">
        <a href=${document.URL.includes("index.html") ? link : linkTwo}
          ><img class="props_img" src=${image && imageTwo} alt=""
        /></a>
        <div class="property_info">
          <span>$${price}</span>
          <p>${location}</p>
        </div>
      </div>
        `;
  }
);

console.log(property.length);
const parentContainer = document.querySelector(".properties_grid");
for (let index = 0; index < property.length; index++) {
  parentContainer.innerHTML += property[index];
}

let imagesArray;
let dataDb;
const imageClick = document.querySelectorAll(".props_img");
imageClick.forEach((image) => {
  image.onclick = (e) => {
    imagesArray = e.target.src;
    localStorage.setItem("data", imagesArray);
  };
});
let getDb = localStorage.getItem("data");
const pageList = document.querySelector(".property_image img");
pageList.src = getDb;
// pageList.parentElement.style.width =
//   window.innerWidth - window.innerWidth * 0.1 + "px";
if (window.innerWidth < 450) {
  if(document.URL.includes("index.html")){
    pageList.style = true;
  }else{
    pageList.style.height = window.innerWidth - window.innerWidth * 0.1 + "px";
  }
}
