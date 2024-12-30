import {HttpException, HttpStatus, Injectable, UnauthorizedException} from '@nestjs/common';
import {LoginUserDto} from "../users/dto/login-user.dto";
import {CreateUserDto} from "../users/dto/create-user.dto";
import {UsersService} from "../users/users.service";
import {JwtService} from "@nestjs/jwt";
import * as bcrypt from 'bcryptjs'
import {User} from "../users/users.model";

@Injectable()
export class AuthService {
    constructor(private userService: UsersService, private jwtService: JwtService) {}

    async login(userDto: LoginUserDto) {
        const user = await this.validateUser(userDto)
        return this.generateToken(user)
    }

    async registration(userDto: CreateUserDto) {
        const candidate = await this.userService.getUserByUsername(userDto.username);
        if (candidate) {
            throw new HttpException("User with this username already exists", HttpStatus.BAD_REQUEST);
        }
        const hashPassword = await bcrypt.hash(userDto.password, 6);
        const user = await this.userService.createUser({...userDto, password: hashPassword});
        return this.generateToken(user)
    }

    private async generateToken(user: User){
        const payload = {username: user.username, id: user.id};
        return {
            token: this.jwtService.sign(payload)
        }
    }

    private async validateUser(userDto: LoginUserDto) {
        const user = await this.userService.getUserByUsername(userDto.username);
        if(!user){
            throw new HttpException("User not exist", HttpStatus.BAD_REQUEST);
        }
        const passwordIsEquals = await bcrypt.compare(userDto.password, user.password);
        if(!passwordIsEquals){
            throw new UnauthorizedException({message: "Password is incorrect"});
        }
        return user
    }
}
