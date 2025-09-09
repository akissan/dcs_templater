function draw_lines(controller, data) {
  console.log("Looking for ", controller);
  const controller_container = document.getElementById(`${controller}_view`);

  if (controller_container) {
    console.log("Success", controller_container);
  } else {
    return "what?";
  }

  const svg_layer = controller_container
    .getElementsByClassName("lineoverlay")
    .item(0);
  svg_layer.replaceChildren();
  const controller_img = controller_container
    .getElementsByClassName("controller_img")
    .item(0);

  const zoomFactor = {
    x: controller_img.width / controller_img.naturalWidth,
    y: controller_img.height / controller_img.naturalHeight,
  };

  for (const [section, controls] of Object.entries(data)) {
    console.log(section);

    for (const [control_name, control_data] of Object.entries(controls)) {
      console.log(control_name, control_data["meta"]);

      if (control_data["meta"]) {
        let { x, y } = control_data["meta"];

        const x1 = x * zoomFactor.x;
        const y1 = y * zoomFactor.y;

        const newLine = document.createElementNS(
          "http://www.w3.org/2000/svg",
          "line"
        );

        const element = controller_container.querySelector(
          `[data-controller="${control_name}"]`
        );

        const box = element.getBoundingClientRect();
        let x2 = box.x - svg_layer.getBoundingClientRect().x;
        let y2 = box.y - svg_layer.getBoundingClientRect().y;

        if (section == "top" || section == "down") {
          x2 += box.width * 0.5;

          if (section == "top") {
            y2 += box.height;
          }
        }

        if (section == "left" || section == "right") {
          y2 += box.height * 0.5;

          if (section == "left") {
            x2 += box.width;
          }
        }

        newLine.setAttribute("id", "line2");
        newLine.setAttribute("x1", x1);
        newLine.setAttribute("y1", y1);

        console.log(x2, controller_img.width);

        if (x2 < 0) {
          x2 = 4;
        }

        newLine.setAttribute("x2", x2);
        newLine.setAttribute("y2", y2);
        newLine.setAttribute("stroke-width", 2);
        newLine.setAttribute("stroke-linecap", "round");
        newLine.setAttribute("stroke", "currentColor");

        // if (x2 < controller_img.getBoundingClientRect().left) {
        //   x2 = controller_img.getB
        // }

        svg_layer.append(newLine);
      }
    }
  }
}

function draw_controller_lines() {
  for (const [controller, data] of Object.entries(window.data)) {
    draw_lines(controller, data);
  }
}

window.addEventListener("load", draw_controller_lines);
window.addEventListener("resize", draw_controller_lines);
