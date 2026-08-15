import {
  Scale,
  CircleCheck,
} from "lucide-react";


function Navbar() {

  return (
    <header className="navbar">

      <div className="brand">

        <div className="brand-icon">
          <Scale size={22} />
        </div>

        <div>
          <div className="brand-name">
            NyayAI
          </div>

          <div className="brand-subtitle">
            Legal Research Assistant
          </div>
        </div>

      </div>


      <div className="system-status">

        <CircleCheck size={15} />

        <span>
          System Online
        </span>

      </div>

    </header>
  );
}


export default Navbar;
